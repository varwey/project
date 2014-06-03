SELECT DISTINCT  name
FROM    keyword 
WHERE   type in (0, 1, 2, 5) and enabled = 1
ORDER BY type, priority DESC;
