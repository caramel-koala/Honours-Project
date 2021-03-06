# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 10:29:03 2016

@author: caramelkoala

Performs the divide part of the divide and conquer
"""

import shape as sh
from merge import merge

def Voronoi(points,range_points):
	"""
	points: complete list of points to be used for tessellation
	range_points: the range of points over which to generate a voronoi
  
  return: A voronoi structure (list of lists) containing a series of centres, lines and the connections between them
	"""
# if Voronoi is singular, send it back with the entire plane as it's facet
	if (range_points[0]==range_points[1]):
		print('Single element Voronoi, no tesellation to be done')
		return [None, range_points,sh.amc(points,range_points)]
     
# If Voronoi has two elements return the plane divided in two based on the element's position
	elif (range_points[1]-range_points[0]+1) == 2:
		lower = range_points[0]
		upper = range_points[1]
		line = [sh.biSector(points[lower],points[upper])]
		line[0][2] = points[lower]
		line[0][3] = points[upper]
		
		points[lower][6].append([line[0],points[upper]])
		points[upper][6].append([line[0],points[lower]])
		
		return [line,range_points,sh.amc(points,range_points)]
		
# If the Voronoi has 3 elements, divide it in 3 and return the structure
	elif (range_points[1]-range_points[0]+1) == 3:
		lower = range_points[0]
		upper = range_points[1]
		lines = []
		dis = []
		t = 0
		mid = []
		for i in range(lower,upper):
			for j in range(i+1,upper+1):
				lines.append(sh.biSector(points[i],points[j]))
				points[i][6].append([lines[-1],points[j]])
				points[j][6].append([lines[-1],points[i]])
				lines[-1][2] = points[i]
				lines[-1][3] = points[j]
				mid.append(((float(points[i][0]+points[j][0])/2,float(points[i][1]+points[j][1])/2),t))
				dis.append((t,(points[i][0]-points[j][0])**2+(points[i][1]-points[j][1])**2,sh.NewLine(points[i],points[j])))
				t = t+1
				
		circumcenter = sh.Intersect(lines[0],lines[1])
		if circumcenter is not None:
			tmp_lines = None
			dis.sort(key = lambda x : x[1])
			triangle = 'acute'
			if dis[0][1]+dis[1][1] == dis[2][1]:
				triangle = 'right'
				tmp_lines = dis[0:2]
			elif dis[0][1]+dis[1][1]<dis[2][1]:
				triangle = 'obtuse'
	
	
			s = dis[2][0]
			t = 0
	
			for i in range(lower,upper):
				for j in range(i+1,upper+1):
					ab = (sh.NewLine(points[i],points[j]))
					hl = sh.NewLine(lines[t][0],circumcenter)
					result = sh.Intersect(hl,ab)
	
					#do not determine the longest side of right triangle in the same way
					if not (triangle == 'right' and t == s):
						if result  is  None:
							#reverse policy for longest side of obtuse
							if not (triangle == 'obtuse' and t == s):
								lines[t][0] = circumcenter
							else:
								lines[t][1] = circumcenter
						else:
							if not (triangle == 'obtuse' and t == s):
								lines[t][1] = circumcenter
							else:
								lines[t][0] = circumcenter
					t = t+1
			#now determine the longest side of right triangle
			if triangle == 'right':
				t = dis[2][0]
				if sh.Intersect(sh.NewLine(lines[t][0],circumcenter),tmp_lines[0][2])  != None or sh.Intersect(sh.NewLine(lines[t][0],circumcenter),tmp_lines[1][2]) != None:
					lines[t][0],lines[t][1] = circumcenter,lines[t][1]
				else:
					lines[t][0],lines[t][1] = circumcenter,lines[t][0]
	
			#create circumcenter related points
			circumcenter[3] = True
			lines[0][5].append(lines[1])
			lines[0][5].append(lines[2])
			lines[1][5].append(lines[0])
			lines[1][5].append(lines[2])
			lines[2][5].append(lines[0])
			lines[2][5].append(lines[1])
			
		else:
			mid.sort(key = lambda s: s[1])
			mid.sort(key = lambda s: s[0])
			t = mid[1][1]
			del_line = lines[t]
			for i in range(lower,upper+1):
				u = points[i][6]
				for j in range(0,len(u)):
					if u[j][0] is del_line:
						del u[j]
						break
			del lines[t]
			
		return [lines,range_points,sh.amc(points,range_points)]

# Finally, if there are more than 3 elements, divide the set in two, recursively call the Voronoi creator, merge the two Voronoi's and return the completed structure
	else:
		mid = int((range_points[1]+range_points[0])/2)
		VDL = Voronoi(points,(range_points[0],mid))

		VDR = Voronoi(points,(mid+1,range_points[1]))
		merge_vd = merge(points,VDL,VDR)
		return merge_vd