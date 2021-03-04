from fabric.api import local, cd, run, env, prefix

env.hosts = ['cloud']


def deploy():
    local('git push')
    with prefix('source ~/.virtualenvs/python-ucticee/bin/activate'):
        with cd('~/code/python-ucticee'):
            run('git pull')
            run('pip install -r requirements.txt')
            run('make dirhtml')
