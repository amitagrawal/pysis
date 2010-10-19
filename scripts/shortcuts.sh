
# Add this file to your ~/.bashrc
# Example :
#    . ~/scripts/pysis/scripts/shortcuts.sh

function pysis()
{
    workon pysis
    cd ~/scripts/pysis
    export DJANGO_SETTINGS_MODULE=pysis.settings.settings
    scripts/restart_webserver.sh
}
