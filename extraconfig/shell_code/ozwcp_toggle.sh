#!/bin/bash

BIN_FOLDER=/srv/homeassistant/src/open-zwave-control-panel/
if [ -z $2 ]; then
	PORT=8888
else
	PORT=$2
fi

test -f ${BIN_FOLDER}ozwcp || exit 0
case "$1" in
    start)
            echo -n "Starting ozwcp"
            cd ${BIN_FOLDER}
            nohup ./ozwcp -p${PORT} > /dev/null 2>&1 &
            echo $! > ${BIN_FOLDER}ozwcp.pid
            echo ""
            ;;
     stop)
            echo -n "Stopping ozwcp"
            rm -f ${BIN_FOLDER}ozwcp.pid
            pkill ozwcp
            echo ""
            ;;
     toggle)
            if [ -f "${BIN_FOLDER}ozwcp.pid" ];then
                    rm -f ${BIN_FOLDER}ozwcp.pid
		    pkill ozwcp
                    echo "Stopped ozwcp (was running)"
                    echo ""
            else
                    cd ${BIN_FOLDER}
                    nohup ./ozwcp -p${PORT} > /dev/null 2>&1 &
                    echo $! > ${BIN_FOLDER}ozwcp.pid
                    echo "Started ozwcp (was stopped)"
                    echo ""
            fi
            ;;
        *)
            echo "Usage: ./ozwcp_toggle.sh start|stop|toggle <portnumber>"
            exit 1
            ;;
esac
