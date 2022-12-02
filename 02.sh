# aocd 02 2022 > input02.txt

SUM=0
while read opponent player; do
  opp=$(echo $opponent | tr 'ABC' '123')
  you=$(echo $player | tr 'XYZ' '123')
  SUM=$((s=$SUM, y=$you, o=$opp, s+y+((y-o+1)%3)*3))
done <input02.txt

echo $SUM #8665 should be 8890


