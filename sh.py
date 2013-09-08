import subprocess

def sh(script):
    """
    Opens bash shell subprocess; returns stdout(0), stderr(1), PID(2), and returncode(3) in a respective list
    """

    p = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    ret = [out, err, p.pid, p.returncode]
    
    return ret