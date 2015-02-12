-- Table collecting awards into one table
create table awardsknn2 as
select a.playerID as playerID, m.MVP as MVP, c.Cy_Young as Cy_Young, g.Gold_Glove as Gold_Glove, h.inducted as inducted
from awardsplayers a
left outer join (
select playerID, count(awardID) as MVP
from awardsplayers
where awardID = 'Most Valuable Player'
group by playerID) m
on a.playerID = m.playerID
left outer join (
select playerID, count(awardID) as Cy_Young
from awardsplayers
where awardID = 'Cy Young Award'
group by playerID) c
on a.playerID = c.playerID
left outer join (
select playerID, count(awardID) as Gold_Glove
from awardsplayers
where awardID = 'Gold Glove'
group by playerID) g
on a.playerID = g.playerID
left outer join (
select playerID, inducted
from halloffame) h
on a.playerID = h.playerID
where h.inducted is not null
group by a.playerID
order by a.playerID asc