#! /bin/sh

set -e 

do_one_service() {
    #Usage: do_one_service service
    service=$1
    name=$service
    binrpm=$(ls RPMS/${name}*)
    srpm=$(ls SRPMS/${name}*)
    spec=$(ls SPECS/${name}*)

    sed -e "s}NAME}$name}" \
	-e "s}BINRPM}$binrpm}" \
	-e "s}SRPM}$srpm}" \
	-e "s}SPEC}$spec}" \
	template.html > $name.html
}

for i in $@; do
    do_one_service $i
done
