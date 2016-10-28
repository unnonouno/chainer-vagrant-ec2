import fabric
from fabric.api import cd, env, put, run, sudo, shell_env


def apt_update():
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('apt-get update -y -qq')
        sudo('apt-get upgrade -y -qq')


def install_nvidia():
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('apt-get install -yq linux-image-extra-`uname -r`')
        sudo('add-apt-repository -y ppa:graphics-drivers/ppa')
        sudo('apt-get -y update')
        sudo('apt-get -yq install nvidia-367 nvidia-settings')


def install_cuda80_deb():
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        deb_file = 'cuda-repo-ubuntu1604-8-0-local_8.0.44-1_amd64-deb'
        url = 'https://developer.nvidia.com/compute/cuda/8.0/prod/local_installers/%s' % deb_file
        run('wget -q %s' % url)
        sudo('dpkg -i %s' % deb_file)
        sudo('apt-get update -yq')
        sudo('apt-get install -yq cuda')
        run('echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bash_profile')
        fabric.operations.reboot()

def install_cuda75_deb():
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        deb_file = 'cuda-repo-ubuntu1404-7-5-local_7.5-18_amd64.deb'
        url = 'http://developer.download.nvidia.com/compute/cuda/7.5/Prod/local_installers/%s' % deb_file
        run('wget -q %s' % url)
        sudo('dpkg -i %s' % deb_file)
        sudo('apt-get update -yq')
        sudo('apt-get install -yq cuda')
        run('echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bash_profile')
        fabric.operations.reboot()


def install_cuda70_deb():
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        deb_file = 'cuda-repo-ubuntu1404-7-0-local_7.0-28_amd64.deb'
        url = 'http://developer.download.nvidia.com/compute/cuda/7_0/Prod/local_installers/rpmdeb/%s' % deb_file

        run('wget -q %s' % url)
        sudo('dpkg -i %s' % deb_file)
        sudo('apt-get update -yq')
        sudo('apt-get install -yq cuda')
        run('echo "export PATH=/usr/local/cuda/bin:$PATH" >> ~/.bash_profile')
        fabric.operations.reboot()


def _install_cudnn(ver, cudnn):
    url = 'http://developer.download.nvidia.com/compute/redist/cudnn/%s/%s' % (ver, cudnn)
    run('wget -q %s' % url)
    sudo('tar -xzf %s -C /usr/local' % cudnn)
    run('rm %s' % cudnn)
    sudo('ldconfig')


def install_cudnn5():
    _install_cudnn('v5.1', 'cudnn-8.0-linux-x64-v5.1.tgz')

def install_cudnn4():
    _install_cudnn('v4', 'cudnn-7.0-linux-x64-v4.0-prod.tgz')


def install_cudnn3():
    _install_cudnn('v3', 'cudnn-7.0-linux-x64-v3.0-prod.tgz')


def install_cudnn2():
    _install_cudnn('v2', 'cudnn-6.5-linux-x64-v2.tgz')


def install_chainer_env():
    sudo('apt-get install -yq g++ libhdf5-dev python-dev python-pip')
    sudo('pip install -U setuptools pip')
    sudo('pip install h5py')
    sudo('pip install numpy')


def install_chainer():
    apt_update()
    install_nvidia()
    install_cuda80_deb()
    install_cudnn5()
    install_chainer_env()
    sudo('pip install chainer')

    # On ubuntu16.04, lightdb runs out of cpu.
    sudo('systemctl disable lightdm')


def install_chainer_dev():
    apt_update()
    install_nvidia()
    install_cuda75_deb()
    install_cudnn4()
    install_chainer_env()
    sudo('apt-get install -yq git')
    sudo('pip install cython')
    run('git clone https://github.com/pfnet/chainer.git')
