use aquarium;

-- Check animals report to see animals’ feeding status
select *
from animal;


-- Update animal feeding status
update animal
set status = true
where an_ID = '103001';


-- Check facility to see facility availability
select fa_ID , f.name
from facility f
left join animal on f.fa_id = animal.habitat
where species = 'spotted seal' or (f.fa_ID not in (select habitat from animal group by habitat) and f.fa_ID not in (select e.facility from event e group by e.facility))
group by fa_ID;


-- Add new animal
insert into animal values ('106001', 'Winston', 'bottlenose dolphin', 0, '705628448', '100005');


-- Remove existing animal
-- delete from animal where an_ID = '103001';
