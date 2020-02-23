#!/bin/bash

. /etc/houyi_pet/lib/houyi/db.sh

function main()
{
     local snapshot_id=$1
     local cluster_id=$(echo $snapshot_id | awk -F- '{print $1}')

     local sql="select cluster_name from zone where cluster_id = '$cluster_id'"
     local cluster_name=$(houyiregiondb -Ne "$sql")

     local output_dir='/apsarapangu/disk1/tmp_image'
     if [ ! -d $output_dir ]; then
         mkdir -p $output_dir
     fi

     sql="select driver from snapshot where logical_id = '$snapshot_id'"
     local driver=$(houyiregiondb -Ne "$sql")

     sql="select access_id, access_key, ocm_addr, domain from oss_info where url like '%$cluster_name%'"
     local oss_info=$(houyiregiondb -Ne "$sql")

     local access_id, access_key, ocm_addr, oss_domain
     access_id=$(echo $oss_info | awk '{print $1}')
     access_key=$(echo $oss_info | awk '{print $2}')
     ocm_addr=$(echo $oss_info | awk '{print $3}')
     oss_domain=$(echo $oss_info | awk '{print $4}')

     local cmd="/opt/tdc/tdc_admin rs --snapshot_id=$snapshot_id --oss_snapshot_domain=$oss_domain \
               --oss_access_id=$access_id --oss_access_key=$access_key --oss_ocm_address=$ocm_addr \
               --dump_data=true --output=$output_dir/$snapshot_id.$driver"

     echo $cmd
     $cmd
}

if [ "$#" != "1" ]; then
    cat << EOF
sh $0 <snapshot_id>
EOF
    exit 1
fi

main $1

