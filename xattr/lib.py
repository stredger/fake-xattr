import os
import sys
import fcntl
import cPickle

XATTR_NOFOLLOW = 1
XATTR_CREATE = 2
XATTR_REPLACE = 4
XATTR_NOSECURITY = 8
XATTR_MAXNAMELEN = 1024
XATTR_FINDERINFO_NAME = False
XATTR_RESOURCEFORK_NAME = False

xattr_dir = '/etc/swift/xattrs'


def get_inode_from_path(path):
    return str(os.stat(path).st_ino)

def get_inode_from_fd(fd):
    return str(os.fstat(fd).st_ino)

def get_xattr_path(f):
    return os.path.join(xattr_dir, f)

def get_xattr_dict(xf):
    try: return cPickle.load(xf)
    except EOFError: return {}

def write_xattr_dict(d, xf):
    cPickle.dump(d, xf)



def _igetxattr(inode, name):
    xattr_fname = get_xattr_path(inode)
    if not os.path.exists(xattr_fname): 
        raise IOError('Failed to get xattr')
    xf = open(xattr_fname)
    fcntl.flock(xf, fcntl.LOCK_SH)
    xattrs = get_xattr_dict(xf)
    fcntl.flock(xf, fcntl.LOCK_UN)
    xf.close()
    xattr = xattrs.get(name, None)
    if xattr: return xattr
    raise IOError('Failed to get xattr')


def _getxattr(path, name, size=0, position=0, options=0):
    """
    getxattr(path, name, size=0, position=0, options=0) -> str
    """
    inode = get_inode_from_path(path)
    return _igetxattr(inode, name)


def _fgetxattr(fd, name, size=0, position=0, options=0):
    """
    fgetxattr(fd, name, size=0, position=0, options=0) -> str
    """
    inode = get_inode_from_fd(fd)
    return _igetxattr(inode, name)



def _isetxattr(inode, name, val):
    xattr_fname = get_xattr_path(inode)
    if os.path.exists(xattr_fname): created = False
    else: created = True
    if not created:
        xf = open(xattr_fname)
        fcntl.flock(xf, fcntl.LOCK_SH)
        xattrs = get_xattr_dict(xf)
        fcntl.flock(xf, fcntl.LOCK_SH)
        xf.close()
    else: xattrs = {} 
    xattrs[name] = val
    xf = open(xattr_fname, 'w+')
    fcntl.flock(xf, fcntl.LOCK_EX)
    write_xattr_dict(xattrs, xf)
    fcntl.flock(xf, fcntl.LOCK_UN)
    xf.close()


def _setxattr(path, name, value, position=0, options=0):
    """
    setxattr(path, name, value, position=0, options=0) -> None
    """
    inode = get_inode_from_path(path)
    _isetxattr(inode, name, value)


def _fsetxattr(fd, name, value, position=0, options=0):
    """
    fsetxattr(fd, name, value, position=0, options=0) -> None
    """
    inode = get_inode_from_fd(fd)
    _isetxattr(inode, name, value)



def _iremovexattr(inode, name):
    xattr_fname = get_xattr_path(inode)
    if not os.path.exists(xattr_fname): 
        raise IOError('Failed to remove xattr')
    else: xf = open(xattr_fname, 'r')
    fcntl.flock(xf, fcntl.LOCK_SH)
    xattrs = get_xattr_dict(xf)
    fcntl.flock(xf, fcntl.LOCK_UN)
    xf.close()
    if name not in xattrs.keys():
        raise IOError('Failed to remove xattr')
    xattrs.pop(name)
    xf = open(xattr_fname, 'w+')
    fcntl.flock(xf, fcntl.LOCK_EX)
    write_xattr_dict(xattrs, xf)
    fcntl.flock(xf, fcntl.LOCK_UN)
    xf.close()
    

def _removexattr(path, name, options=0):
    """
    removexattr(path, name, options=0) -> None
    """
    inode = get_inode_from_path(path)
    _iremovexattr(inode, name)



def _fremovexattr(fd, name, options=0):
    """
    fremovexattr(fd, name, options=0) -> None
    """
    inode = get_inode_from_fd(fd)
    _iremovexattr(inode, name)


def _ilistxattr(inode):
    xf_name = get_xattr_path(inode)
    if not os.path.exists(xf_name): 
        raise IOError('Failed to get xattr')
    xf = open(xf_name)
    fcntl.flock(xf, fcntl.LOCK_SH)
    xattrs = get_xattr_dict(xf)
    fcntl.flock(xf, fcntl.LOCK_UN)
    xf.close()
    return list(xattrs)

def _listxattr(path, options=0):
    """
    listxattr(path, options=0) -> str
    """
    inode = get_inode_from_path(path)
    return _ilistxattr(inode)


def _flistxattr(fd, options=0):
    """
    flistxattr(fd, options=0) -> str
    """
    inode = get_inode_from_fd(fd)
    return _ilistxattr(inode)
