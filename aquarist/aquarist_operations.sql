use aquarium;


-- Check facility maintenance schedule
-- input variable: staff ID of the aquarist
--    main python program should hold st_id value taken at login
select name as 'Facility', fa_id as 'ID', maint_time as 'Maintenance Time'
from facility_maint
left join facility on facility.fa_id = facility_maint.facility
left join maintain on fa_id = maintain.facility
where maint_status = FALSE
and staff = '987153744'
order by maint_time;

-- Change status
-- input variables: facility ID and time slot
update facility_maint
set maint_status = true
where facility = '333333'
and maint_time = '12:00:00';

-- reset maint_status
update facility_maint
set maint_status = false
where facility is not null;

-- check table
select *
from facility_maint;

