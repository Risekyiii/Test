#!/bin/bash


units=$(systemctl list-units --type=service --all --quiet --no-pager | grep '^foobar-' | awk '{print $1}')


for unit in $units; do
    echo "Обрабатываем юнит: $unit"


    service_name=$(echo "$unit" | sed 's/^foobar-//')

    
    old_working_dir="/opt/misc/$service_name"
    new_working_dir="/srv/data/$service_name"
    old_exec_start="/opt/misc/$service_name/foobar-daemon"
    new_exec_start="/srv/data/$service_name/foobar-daemon"

 
    echo "Останавливаем юнит $unit"
    systemctl stop "$unit"

    
    echo "Переносим файлы из $old_working_dir в $new_working_dir"
    mv "$old_working_dir" "$new_working_dir"

    
    echo "Обновляем параметры юнита $unit"
    unit_file="/etc/systemd/system/$unit.service"

    
    cp "$unit_file" "${unit_file}.bak"

    
    sed -i "s|WorkingDirectory=$old_working_dir|WorkingDirectory=$new_working_dir|" "$unit_file"
    sed -i "s|ExecStart=$old_exec_start|ExecStart=$new_exec_start|" "$unit_file"

    
    echo "Перезагружаем systemd для учета изменений"
    systemctl daemon-reload

    
    echo "Запускаем юнит $unit"
    systemctl start "$unit"
done

echo "Все юниты были успешно обработаны!"