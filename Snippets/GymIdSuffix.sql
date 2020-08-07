/*
query to examine gym_id suffix
length of 32 is sponsored
length of 35 is normal
*/
SELECT LENGTH(gym_id),gym_id,NAME,
if(length(gym_id)>32,RIGHT(gym_id,2),"") AS suffix 
FROM gymdetails ORDER BY suffix,gym_id
