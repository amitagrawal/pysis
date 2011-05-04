
# Add this file to your ~/.bashrc
# Example :
#    . ~/scripts/pysis/scripts/shortcuts.sh

function pysis()
{
    workon pysis
    cd /work/pysis
    export DJANGO_SETTINGS_MODULE=pysis.settings.settings

    sudo supervisorctl restart pysis
}
