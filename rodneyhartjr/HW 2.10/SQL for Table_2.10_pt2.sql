-- Part 1
select playerID, yearID, sum(R) as total_runs, sum(H) as total_hits, sum(SB) as stolen_bases, sum(SO) as strikeouts, sum(IBB) as total_intentional_walks
from Batting 
where yearID > 1954
and yearid < 2005
group by playerID
order by playerID ASC;

-- Part 2
select playerID, yearID, sum(R) as total_runs, sum(H) as total_hits, sum(SB) as stolen_bases, sum(SO) as strikeouts, sum(IBB) as total_intentional_walks
from Batting 
where yearID >= 2005
group by playerID
order by playerID ASC;