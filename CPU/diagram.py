# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:20:07 2016

@author: caramelkoala
"""

import ch as ch
import shape as sh
from collections import defaultdict

def merge(points,VDL,VDR):
    clip_lines = []
    #used to record ray which intersect with dividing chain
    #using hash table
    ray_list = []
    
    def discard_edges(ray,circumcenter,side,SG_bisector):

        def recursive_discard_edge(ray,other_point,base_point,side):
            #want to delete left remaining line
            for candidate in ray[5]:
                if candidate[6] == True and candidate not in ray_list:
                    next_base_point = None
                    next_other_point = None
                    #catch base point
                    if(candidate[0] is base_point or candidate[1] is base_point):
                        if candidate[0] is base_point:
                            next_base_point = candidate[1]
                            next_other_point = candidate[0]
                        else:
                            next_base_point = candidate[0]
                            next_other_point = candidate[1]

                        if side == 'right':
                            if sh.cross(base_point,next_base_point,other_point) > 0:
                                candidate[6] = False
                                recursive_discard_edge(candidate,next_other_point,next_base_point,'right')
                        elif side == 'left':
                            if sh.cross(base_point,next_base_point,other_point) < 0:
                                candidate[6] = False
                                recursive_discard_edge(candidate,next_other_point,next_base_point,'left')

        if side == 'right':
            #clear the edges extend to the left of HP
            #Line(hole,ray.p1) or Line(hole,ray.p2) must cw to Line(hole,bisector.p1)
            if sh.cross(circumcenter,ray[0],SG_bisector[0])>0:
                #this means p1 is left to circumcenter,so replace p1 with circumcenter
                if ray[0][3] == True:
                    recursive_discard_edge(ray,circumcenter,ray[0],'right')
                ray[0] = circumcenter
            else:
                if ray[1][3] == True:
                    recursive_discard_edge(ray,circumcenter,ray[1],'right')
                ray[1] = circumcenter
        elif side == "left":
            #clear the edges extend to the right of HP
            #Line(hole,ray.p1) or Line(hole,ray.p2) must ccw to Line(hole,bisector.p1)
            if sh.cross(circumcenter,ray[0],SG_bisector[0])<0:
                #this means p1 is right to circumcenter,so replace p1 with circumcenter
                if ray[0][3] == True:
                    recursive_discard_edge(ray,circumcenter,ray[0],'left')
                ray[0] = circumcenter
            else:

                if ray[1][3] == True:
                    recursive_discard_edge(ray,circumcenter,ray[1],'left')
                ray[1] = circumcenter
        else:
            #clear both side
            #clear the edges extend to the right of HP
            #Line(hole,ray.p1) or Line(hole,ray.p2) must ccw to Line(hole,bisector.p1)
            if sh.cross(circumcenter,ray[0][0],SG_bisector[0])<0:
                #this means p1 is right to circumcenter,so replace p1 with circumcenter
                if ray[0][0][3] == True:
                    recursive_discard_edge(ray[0],circumcenter,ray[0][0],'left')
                ray[0][0] = circumcenter
            else:
                if ray[0][1][3] == True:
                    recursive_discard_edge(ray[0],circumcenter,ray[0][1],'left')
                ray[0][1] = circumcenter

            #clear the edges extend to the left of HP
            if sh.cross(circumcenter,ray[1][0],SG_bisector[0])>0:
                #this means p1 is left to circumcenter,so replace p1 with circumcenter
                if ray[1][0][3] == True:
                    recursive_discard_edge(ray[1],circumcenter,ray[1][0],'right')
                ray[1][0] = circumcenter
            else:
                if ray[1][1][3] == True:
                    recursive_discard_edge(ray[1],circumcenter,ray[1][1],'right')
                ray[1][1] = circumcenter

    def nextPoint(pool,SG_bisector):
        ans = None
        first = True
        for candidate in pool:
            if candidate[0][6] == True and SG_bisector[0] is not candidate[0][4]:
                result = sh.Intersect(candidate[0],SG_bisector)
                if result is not None:
                    t = (result,candidate[1],candidate[0])
                    if first ==  True:
                        ans = t
                        first = False
                    else:
                        if t[0][1] <= ans[0][1]:
                            ans = t
        return ans

    upper_tangent,lower_tangent = find_tangent(points,VDL,VDR)
#    ul = (upper_tangent,lower_tangent)
#    tangent[0].append(ul)

    HP = []
    SG = upper_tangent
    px = SG[0]
    py = SG[1]
    #p1 of upper_tangent belongs to VDL, and p2 belongs to VDR
    SG_bisector = sh.biSector(SG[0],SG[1])
    SG_bisector[2] = SG[0]
    SG_bisector[3] = SG[1]

    HP.append(SG_bisector)
    circumcenter = None

    firsttime = True
    newpl = []

    while not (SG  == lower_tangent):
        #step4 as textBook

        #p1 of SG_bisector is fixed to upper position than p2
        if SG_bisector[0][1] > SG_bisector[1][1]:
            SG_bisector[0],SG_bisector[1] = SG_bisector[1],SG_bisector[0]
        elif abs((SG_bisector[0][1])-(SG_bisector[1][1])) <= 0.00005:
            if SG_bisector[0][0]<SG_bisector[1][0]:
                SG_bisector[0],SG_bisector[1] = SG_bisector[1],SG_bisector[0]

        newpl.append([SG[0],SG_bisector,SG[1]])
        newpl.append([SG[1],SG_bisector,SG[0]])

        #orginally p1 is very far from painter,so we need to fix p1 to previous circumcenter
        if firsttime == False and circumcenter is not None:
            SG_bisector[0] = circumcenter

        pll = px[6]
        prl = py[6]

        result_l = nextPoint(pll,SG_bisector)
        result_r = nextPoint(prl,SG_bisector)

        side = None
        ray = None
        #with biSector of pyz2 first,that is,VDR first
        if result_l is not None and result_r is not None:
            if abs(result_l[0][0]-result_r[0][0]) <= 0.05 and abs(result_l[0][1]-result_r[0][1]) <= 0.05:
                #VDL.parent.msg = VDL.parent.msg+'both cd'+'\n'
                SG = sh.NewLine(result_l[1],result_r[1]);
                circumcenter = result_l[0]
                ray = (result_l[2],result_r[2])
                side = 'both'
            elif result_l[0][1] > result_r[0][1]:
                #VDL.parent.msg = VDL.parent.msg+'cd VDR'+'\n'
                SG = sh.NewLine(px,result_r[1])
                circumcenter = result_r[0]
                ray = result_r[2]
                side = 'right'
            elif result_l[0][1] < result_r[0][1]:
                #VDL.parent.msg = VDL.parent.msg+'cd VDL'+'\n'
                SG = sh.NewLine(result_l[1],py)
                circumcenter = result_l[0]
                ray = result_l[2]
                side = 'left'
            else:
                print 'confused...'
                #print result_l,result_r
        else:
            if result_l is not None and result_r is None:
                #VDL.parent.msg = VDL.parent.msg+'VDR is None,cd VDL'+'\n'
                SG = sh.NewLine(result_l[1],py)
                circumcenter = result_l[0]
                ray = result_l[2]
                side = 'left'
            elif result_r is not None and result_l is None:
                #VDL.parent.msg = VDL.parent.msg+'VDL is None,cd VDR'+'\n'
                SG = sh.NewLine(px,result_r[1])
                circumcenter = result_r[0]
                #print 'circumcenter',(circumcenter.x,circumcenter.y)
                ray = result_r[2]
                side = 'right'
            else:
                #VDL.parent.msg = VDL.parent.msg+'both are None'+'\n'
                #let SG be lower_tangent
                SG = lower_tangent
                SG_bisector = sh.biSector(SG[0],SG[1])
                SG_bisector[2] = SG[0]
                SG_bisector[3] = SG[1]
                HP.append(SG_bisector)
                continue

        if ray is not None:
            if not isinstance(ray,tuple):
                ray[4] = circumcenter
                t = (ray,SG_bisector,side,circumcenter)
                if ray not in ray_list:
                    ray_list.append(ray)
                clip_lines.append(t)
            else:
                for r in ray:
                    r[4] = circumcenter
                    if r not in ray_list:
                        ray_list.append(r)
                t = (ray,SG_bisector,side,circumcenter)
                clip_lines.append(t)

        if circumcenter is not None:
            circumcenter[3] = True
            #lower point is replaced by circumcenter
            SG_bisector[1] = circumcenter


        #new SG
        px = SG[0]
        py = SG[1]
        SG_bisector = sh.biSector(SG[0],SG[1])
        SG_bisector[2] = SG[0]
        SG_bisector[3] = SG[1]

        HP.append(SG_bisector)
        firsttime = False
        #the end of while loop for HP


    if SG_bisector[0][1] > SG_bisector[1][1]:
        SG_bisector[0],SG_bisector[1] = SG_bisector[1],SG_bisector[0]
    elif abs((SG_bisector[0][1])-(SG_bisector[1][1])) <= 0.00005:
        if SG_bisector[0][0]<SG_bisector[1][0]:
            SG_bisector[0],SG_bisector[1] = SG_bisector[1],SG_bisector[0]


    newpl.append([SG[0],SG_bisector,SG[1]])
    newpl.append([SG[1],SG_bisector,SG[0]])

    for p in newpl:
        p[0][6].append([p[1],p[2]])

    if circumcenter is not None:
        SG_bisector[0] = circumcenter


    #clip the unwanted lines
#    VDL.parent.msg = VDL.parent.msg+ 'clip lines'+'\n'
    for t in clip_lines:
        ray = t[0]
        circumcenter = t[3]
        SG_bisector = t[1]
        side = t[2]
        discard_edges(ray,circumcenter,side,SG_bisector)

    #add new connected line
    s = 0
    for t in range(0,len(HP)-1):
        #need to add the intersected dividing chain
        HP[t][5].append(HP[t+1])
        HP[t+1][5].append(HP[t])
        #need to add the intersected ray
        if s  !=  len(clip_lines):
            if not isinstance(clip_lines[s][0],tuple):
                HP[t][5].append(clip_lines[s][0])
                clip_lines[s][0][5].append(HP[t])
                HP[t+1][5].append(clip_lines[s][0])
                clip_lines[s][0][5].append(HP[t+1])
            else:
                r = clip_lines[s][0]
                HP[t][5].append(r[0])
                r[0][5].append(HP[t])
                HP[t+1][5].append(r[0])
                r[0][5].append(HP[t+1])

                HP[t][5].append(r[1])
                r[1][5].append(HP[t])
                HP[t+1][5].append(r[1])
                r[1][5].append(HP[t+1])

                r[1][5].append(r[0])
                r[0][5].append(r[1])
        s = s+1




    lines = []
    #lines = VDR.lines+VDL.lines+HP
    lines.append(VDR[0])
    lines.append(VDL[0])
    lines.append(HP)
#    if VDL.parent.isstep_by_step == True:
#        hp = []
#        for h in HP:
#            hp.append(Line(Point(h.p1.x,h.p1.y),Point(h.p2.x,h.p2.y)))
#        VDR.parent.hp[0].append(hp)
    #VDR.parent.hp[0].append(copy.deepcopy(HP))
    range_points = (VDL[1][0],VDR[1][1])
    return [lines,range_points,sh.amc(points,range_points)]
    #return VD(lines,points)

def find_tangent(points,VDL,VDR):
    pl = points[VDL[1][1]]
    pr = points[VDR[1][0]]

    #handle collinear point
    while not (isupper_tangent(pl,pr,'left') and isupper_tangent(pl,pr,'right')):
        while not isupper_tangent(pl,pr,'left'):
            pl = pl[5]
        while not isupper_tangent(pl,pr,'right'):
            pr = pr[4]

    upper_tangent = sh.NewLine(pl,pr)

    #VDL.parent.msg = VDL.parent.msg + 'upper_tangent = '+upper_tangent.p1.display+' '+upper_tangent.p2.display+'\n'

    pl = points[VDL[1][1]]
    pr = points[VDR[1][0]]

    while not (islower_tangent(pl,pr,'left') and islower_tangent(pl,pr,'right')):
        while not islower_tangent(pl,pr,'left'):
            pl = pl[4]
        while not islower_tangent(pl,pr,'right'):
            pr = pr[5]


    lower_tangent = sh.NewLine(pl,pr)

    #VDL.parent.msg =  VDL.parent.msg+'lower_tangent = '+lower_tangent.p1.display+' '+lower_tangent.p2.display+'\n'


    return (upper_tangent,lower_tangent)

def isupper_tangent(pl,pr,pos):
    if pos == 'left':
        #because y is reverse in canvas,so we need to reverse the clockwise/clock,debug this is so diffcult...
        return sh.cross(pr,pl,pl[5]) <= 0
    else:
        return sh.cross(pl,pr,pr[4]) >= 0


def islower_tangent(pl,pr,pos):
    if pos == 'left':
        return sh.cross(pr,pl,pl[4]) >= 0
    else:
        return sh.cross(pl,pr,pr[5]) <= 0
