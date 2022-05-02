use aquarium;

SELECT ev_ID, COUNT(staff), facility
FROM event
LEFT JOIN work_on ON event.ev_ID = work_on.event
GROUP BY ev_ID;

SELECT *
FROM event_instance
LEFT JOIN event ON event_instance.event = event.ev_ID
WHERE overseer =  ''
ORDER BY date DESC;