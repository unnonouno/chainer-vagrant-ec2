import fabric
from fabric.api import cd, env, put, run, sudo, shell_env


def apt_update():
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('apt-get update -y -qq')
        sudo('apt-get upgrade -y -qq')


def install_cuda75_deb():
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('apt-get install -yq build-essential')

        sudo('apt-get install -yq linux-source')
        sudo('apt-get install -yq linux-headers-`uname -r`')

        deb_file = 'cuda-repo-ubuntu1404-7-5-local_7.5-18_amd64.deb'
        run('wget -q http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/%s' % deb_file)
        sudo('dpkg -i %s' % deb_file)
        sudo('apt-get update -yq')
        sudo('apt-get install -yq cuda')
        run('echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bash_profile')
        fabric.operations.reboot()


def install_cuda70_deb():
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('apt-get install -yq build-essential')

        sudo('apt-get install -yq linux-source')
        sudo('apt-get install -yq linux-headers-`uname -r`')

        deb_file = 'cuda-repo-ubuntu1404-7-0-local_7.0-28_amd64.deb'
        url = 'http://developer.download.nvidia.com/compute/cuda/7_0/Prod/local_installers/rpmdeb/%s' % deb_file

        run('wget -q %s' % url)
        sudo('dpkg -i %s' % deb_file)
        sudo('apt-get update -yq')
        sudo('apt-get install -yq cuda')
        run('echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bash_profile')
        fabric.operations.reboot()


def _install_cuda(ver, run_file):
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('apt-get install -yq build-essential')

        url = 'http://developer.download.nvidia.com/compute/cuda/%s/Prod/local_installers/%s' % (ver, run_file)
        run('wget -q %s' % url)
        run('chmod +x %s' % run_file)
        run('mkdir nvidia_installers')
        run('./%s -extract=`pwd`/nvidia_installers' % run_file)
        sudo('apt-get install -yq linux-image-extra-virtual')

        put('blacklist-nouveau.conf', '/etc/modprobe.d/', use_sudo=True)
        put('nouveau-kms.conf', '/etc/modprobe.d/', use_sudo=True)
        sudo('update-initramfs -u')

        fabric.operations.reboot()

        sudo('apt-get install -yq linux-source')
        sudo('apt-get install -yq linux-headers-`uname -r`')

        sudo('./%s --silent --driver --toolkit' % run_file)
        sudo('modprobe nvidia')
        run('rm %s' % run_file)
        run('echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bash_profile')


def install_cuda75():
    _install_cuda('7.5', 'cuda_7.5.18_linux.run')


def install_cuda70():
    _install_cuda('7_0', 'cuda_7.0.28_linux.run')


def _install_cudnn(ver, cudnn):
    url = 'http://developer.download.nvidia.com/compute/redist/cudnn/%s/%s' % (ver, cudnn)
    run('wget -q %s' % url)
    sudo('tar -xzf %s -C /usr/local' % cudnn)
    run('rm %s' % cudnn)
    sudo('ldconfig')


def install_cudnn4_rc():
    _install_cudnn('v4', 'cudnn-7.0-linux-x64-v4.0-rc.tgz')


def install_cudnn3():
    _install_cudnn('v3', 'cudnn-7.0-linux-x64-v3.0-prod.tgz')


def install_cudnn2():
    _install_cudnn('v2', 'cudnn-6.5-linux-x64-v2.tgz')


def install_chainer_env():
    sudo('apt-get install -yq g++ libhdf5-dev python-dev python-pip')
    sudo('pip install -U setuptools pip')
    sudo('pip install cython')
    sudo('pip install h5py')
    sudo('pip install numpy')


def install_chainer():
    apt_update()
    install_cuda70()
    install_cudnn3()
    install_chainer_env()
    sudo('pip install chainer')


def install_chainer_dev():
    apt_update()
    install_cuda70()
    install_cudnn3()
    install_chainer_env()
    sudo('apt-get install -yq git')
    run('git clone https://github.com/pfnet/chainer.git')
