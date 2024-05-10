#!/bin/bash

if [ $# -ne 3 ]
then
	echo 'usage: ./2024-OSS-Project.sh file1 file2 file3'
	exit 1
fi

# teams.csv players.csv matches.csv
echo "************OSS1 - Project1************"
echo "*	      StudentID : 12191842          *"
echo "*       Name : DOYUN KIM              *"
echo "***************************************"

stop="N"
OFS=","
until [ "$stop" = "Y" ]
do
	echo "[MENU]"
	echo "1. Get the data of Heung-Min Son's Current Club, Appearances, Goals, Assists in Players.csv"
	echo "2. Get the team data to enter a league position in teams.csv"
	echo "3. Get the Top-3 Attendance matches in mateches.CSV"
	echo "4. Get the team's league position and team's top scorer in teams.CSV & players.csv"
	echo "5. Get the modified format of date_GMT in amtches.csv"
	echo "6. Get the data of the winning team by the largest difference on home stadium in teams.csv & matches.csv"
	echo "7. Exit"
	
	read -p 'Enter your CHOICE (1~7) : ' choice
	
	case "$choice" in
	1)
		ans="u"
		read -p "Do you want to get the Heung-Min Son's data? (y/n) :" ans
		if [ "$ans" = "y" ]
		then
			awk -F, '$1 == "Heung-Min Son"{printf("Team:%s,Apperance:%s,Goal:%s,Assist:%s\n", $4, $6, $7, $8)}' $2
#			awk -F, '{print $3}' $2
		fi
		;;
	2)
		lp=-1
		read -p 'What do you want to get the team data of league_position[1-20]: ' lp
		awk -v lp=$lp -F, '$6 == lp {printf("%s %f\n", $1, $2/($2+$3+$4))}' $1
		;;
	3)
		ans="n"
		read -p 'Do you want to know Top-3 attendance data and average attendance? (y/n) : ' ans
		if [ "$ans" = "y" ]
		then
			echo "***Top-3 Attendance Match***"
			echo ""
#			cat $3 | sed -E 's/(.*),(.*),(.*),(.*),(.*),(.*),(.*)/\2 \1,\3,\4,\7/g' | sort -r -k 1 | 
			cat $3 | sort -n -r -k 2 -t ',' | head -n 3 | awk -F, '{printf("%s VS %s (%s)\n%d %s\n\n", $3, $4, $1, $2, $7)}'
		fi
		;;
	4)
		ans="u"
		read -p "Do you want to get each team's ranking and the highest-scoring player? (y/n) :" ans
		if [ "$ans" = "y" ]
		then
			
			data=$(sort -n -t ',' -k6 "$1")
			echo "$data"
			lineCnt=$(echo "$data" | wc -l)
			echo "$lineCnt"
			i=1
			while (( i < lineCnt )) 
			do
				echo "i $i"
				# i = league position
				echo "$data" | awk -F, -v i="$i" '$6 == i {printf("%s %s\n", $6, $1)}'
				

				# find the best player $2
				m=0
				n=""
				cn=$(echo "$data" | awk -F, -v i="$i" '$6 == i {print $1}')
				echo "$cn"
				while IFS=',' read -r c1 c2 c3 c4 c5 c6 c7 c8
				do 
					name="$c1"
					curClub="$c4"
					mostGoal="$c7"
					mostGoal=$(awk 'BEGIN {print int("'"$mostGoal"'")}')
					if [ "$curClub" == "$cn" ] && [ $m -lt mostGoal ]
					then
						n="$name"
						m="$mostGoal"
					fi
				done < $2

				echo "$n $m"
				
				i=$(( i+1 ))				
			done 
		fi
		;;
	5)
		;;
	6)
		;;
	7)
		stop="Y" ;;
	*)
		echo "ddd";;
	esac
done
