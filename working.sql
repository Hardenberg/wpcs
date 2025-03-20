-- -- SQLite
-- select dnsId_id, count() as d from app_wordpress 
-- where 1=1 
-- group by dnsID_id
-- having d > 1

-- DELETE FROM app_wordpress 
-- WHERE rowid NOT IN (
--     SELECT MIN(rowid) 
--     FROM app_wordpress 
--     GROUP BY dnsId_id
-- );

-- select dns, tld, w.date, ip from app_wordpress as w join app_dns as d  on w.dnsId_id = d.id
-- where 1=1 
--     and user_enumeration = 1
--     and  d.id > 12234
-- limit 100

select * from app_dns
where 1=1
    and dns like "%.%"
    -- and date <= "2025-03-13"
    -- and date >= "2025-03-11"
