import sqlite3, sys

if len(sys.argv) != 3:
    print("Usage:", sys.argv[0], "actor actor")
    sys.exit(1)

if len(sys.argv)==3:
    first=sys.argv[1]
    end=sys.argv[2]

con=sqlite3.connect('a2.db')
cur=con.cursor()

sql_find_aidbyname="select id from actor where lower(name)= '{}'"

sql_find_midbyaid="select movie_id from acting where actor_id={}"

sql_find_moviebymid="select title, year from movie where id={}"

sql_find_namebyaid="select name from actor where id={}"

sql_find_aidbymid="select actor_id from acting where movie_id={}"

sql_intersect=" intersect "

cur.execute(sql_find_aidbyname.format(first.lower()))
firstid=cur.fetchone()
cur.execute(sql_find_aidbyname.format(end.lower()))
endid=cur.fetchone()
# print(firstid,endid)

# first mids
cur.execute(sql_find_midbyaid.format(firstid[0]))
first_mids=cur.fetchall()

# end mids
cur.execute(sql_find_midbyaid.format(endid[0]))
end_mids=cur.fetchall()
# print(first_mids,end_mids)

# common mids
common_mids=[]
for fmid in first_mids:
    first_mid=fmid[0]
    for emid in end_mids:
        end_mid=emid[0]
        if first_mid==end_mid:
            common_mids.append(end_mid)
# print(common_mids)

wasinmovie=" was in "
withactor="with "







if common_mids!=None and len(common_mids)>0:
    # find first
    friends=[]
    cur.execute(sql_find_namebyaid.format(firstid[0]))
    fisrtName =cur.fetchone()
    cur.execute(sql_find_namebyaid.format(endid[0]))
    endName=cur.fetchone()
    for mid in common_mids:
        cur.execute(sql_find_moviebymid.format(mid))
        mtitle, myear=cur.fetchone()
        friends.append(fisrtName[0]+wasinmovie+mtitle+" ("+ str(myear)+ ") "+withactor+endName[0])
    friends.sort()
    count = 1
    for cr in friends:
        print(str(count) + ". " + cr)
        count += 1

else: # find second
    tmp_tuples=[]
    tmp_tuples2 = []
    tmp_tuples3 = []
    cur.execute(sql_find_midbyaid.format(firstid[0]))
    firstmids=cur.fetchall()
    common_results=[]
    for firstmid in firstmids:
        fmid=firstmid[0]
        cur.execute(sql_find_aidbymid.format(fmid))
        aids2=cur.fetchall()
        for aid2 in aids2:
            sql=sql_find_midbyaid.format(aid2[0])+ sql_intersect +sql_find_midbyaid.format(endid[0])
            cur.execute(sql)
            results2=cur.fetchall()
            if results2!=None and len(results2)>0:
                for r2 in results2:
                    common_results.append((firstid[0], fmid, aid2[0], r2[0], endid[0]))
            else:
                # ready for
                cur.execute(sql_find_midbyaid.format(aid2[0]))
                mids2=cur.fetchall()
                for mid2 in mids2:
                    cur.execute(sql_find_aidbymid.format(mid2[0]))
                    aids3=cur.fetchall()
                    for aid3 in aids3:
                        if aid3[0]!=firstid[0] and aid3[0]!=aid2[0]:
                            tuple = (firstid[0], fmid, aid2[0], mid2[0], aid3[0])
                            tmp_tuples.append(tuple)

    if common_results!=None and len(common_results)>0:
        # print(common_results)

        cresults=[]
        for comr in common_results:
            cur.execute(sql_find_namebyaid.format(comr[0]))
            actor1 = cur.fetchone()
            cur.execute(sql_find_moviebymid.format(comr[1]))
            movie1=cur.fetchone()
            cur.execute(sql_find_namebyaid.format(comr[2]))
            actor2 = cur.fetchone()
            cur.execute(sql_find_moviebymid.format(comr[3]))
            movie2=cur.fetchone()
            cur.execute(sql_find_namebyaid.format(comr[4]))
            actor3=cur.fetchone()
            cresults.append(actor1[0]+wasinmovie+movie1[0]+" ("+str(movie1[1])+") "+withactor+actor2[0]+"; "+
                  actor2[0]+wasinmovie+movie2[0]+" ("+str(movie2[1])+") "+ withactor+actor3[0])

        cresults.sort()
        count=1
        for cr in cresults:
            print(str(count)+". "+cr)
            count+=1
    else: #find third
        # print("tmp_tuples",len(tmp_tuples))
        for tp in tmp_tuples:
            aid3=tp[-1]
            sql = sql_find_midbyaid.format(aid3) + sql_intersect + sql_find_midbyaid.format(endid[0])
            cur.execute(sql)
            results3 = cur.fetchall()

            if results3!=None and len(results3)>0:
                for r3 in results3:
                    common_results.append((tp[0], tp[1], tp[2], tp[3],tp[4], r3[0], endid[0]))
            else:
                # ready for
                cur.execute(sql_find_midbyaid.format(aid3))
                mids3=cur.fetchall()
                for mid3 in mids3:
                    cur.execute(sql_find_aidbymid.format(mid3[0]))
                    aids4=cur.fetchall()
                    for aid4 in aids4:
                        if aid4[0]!=tp[0] and aid4[0]!=tp[2] and aid4[0]!=tp[4]:
                            tuple = (tp[0], tp[1], tp[2], tp[3], tp[4], mid3[0], aid4[0])
                            tmp_tuples2.append(tuple)

        if common_results != None and len(common_results) > 0:  # find 3
            cresults = []
            for comr in common_results:
                cur.execute(sql_find_namebyaid.format(comr[0]))
                actor1 = cur.fetchone()
                cur.execute(sql_find_moviebymid.format(comr[1]))
                movie1 = cur.fetchone()
                cur.execute(sql_find_namebyaid.format(comr[2]))
                actor2 = cur.fetchone()
                cur.execute(sql_find_moviebymid.format(comr[3]))
                movie2 = cur.fetchone()
                cur.execute(sql_find_namebyaid.format(comr[4]))
                actor3 = cur.fetchone()
                cur.execute(sql_find_moviebymid.format(comr[5]))
                movie3 = cur.fetchone()
                cur.execute(sql_find_namebyaid.format(comr[6]))
                actor4 = cur.fetchone()
                cresults.append(
                    actor1[0] + wasinmovie + movie1[0] + " (" + str(movie1[1]) + ") " + withactor + actor2[
                        0] + "; " +
                    actor2[0] + wasinmovie + movie2[0] + " (" + str(movie2[1]) + ") " + withactor + actor3[0] + "; " +
                    actor3[0] + wasinmovie + movie3[0] + " (" + str(movie3[1]) + ") " + withactor + actor4[0])

            cresults.sort()
            count = 1
            for cr in cresults:
                print(str(count) + ". " + cr)
                count += 1
        else:  # find 4
            # print("tmp_tuples2",len(tmp_tuples2))
            for tp in tmp_tuples2:
                aid4 = tp[-1]
                sql = sql_find_midbyaid.format(aid4) + sql_intersect + sql_find_midbyaid.format(endid[0])
                cur.execute(sql)
                results4 = cur.fetchall()
                if results4 != None and len(results4) > 0:
                    for r4 in results4:
                        common_results.append((tp[0], tp[1], tp[2], tp[3], tp[4], tp[5], tp[6], r4[0], endid[0]))
                else:
                    # ready for
                    cur.execute(sql_find_midbyaid.format(aid4))
                    mids4 = cur.fetchall()
                    for mid4 in mids4:
                        cur.execute(sql_find_aidbymid.format(mid4[0]))
                        aids5 = cur.fetchall()
                        for aid5 in aids5:
                            tuple = (tp[0], tp[1], tp[2], tp[3], tp[4], tp[5], tp[6], mid4[0], aid5[0])
                            tmp_tuples3.append(tuple)
            if common_results != None and len(common_results) > 0:  # find 4
                cresults = []
                for comr in common_results:
                    cur.execute(sql_find_namebyaid.format(comr[0]))
                    actor1 = cur.fetchone()
                    cur.execute(sql_find_moviebymid.format(comr[1]))
                    movie1 = cur.fetchone()
                    cur.execute(sql_find_namebyaid.format(comr[2]))
                    actor2 = cur.fetchone()
                    cur.execute(sql_find_moviebymid.format(comr[3]))
                    movie2 = cur.fetchone()
                    cur.execute(sql_find_namebyaid.format(comr[4]))
                    actor3 = cur.fetchone()
                    cur.execute(sql_find_moviebymid.format(comr[5]))
                    movie3 = cur.fetchone()
                    cur.execute(sql_find_namebyaid.format(comr[6]))
                    actor4 = cur.fetchone()
                    cur.execute(sql_find_moviebymid.format(comr[7]))
                    movie4 = cur.fetchone()
                    cur.execute(sql_find_namebyaid.format(comr[8]))
                    actor5 = cur.fetchone()
                    cresults.append(
                        actor1[0] + wasinmovie + movie1[0] + " (" + str(movie1[1]) + ") " + withactor + actor2[
                            0] + "; " +
                        actor2[0] + wasinmovie + movie2[0] + " (" + str(movie2[1]) + ") " + withactor + actor3[
                            0] + "; " +
                        actor3[0] + wasinmovie + movie3[0] + " (" + str(movie3[1]) + ") " + withactor + actor4[0]+"; "+
                        actor4[0] +wasinmovie+ movie4[0]+" ("+str(movie4[1])+") "+withactor+actor5[0])

                cresults.sort()
                count = 1
                for cr in cresults:
                    print(str(count) + ". " + cr)
                    count += 1
            else:
                # print("tmp_tuples3", len(tmp_tuples3))
                for tp in tmp_tuples3:
                    aid5 = tp[-1]
                    sql = sql_find_midbyaid.format(aid5) + sql_intersect + sql_find_midbyaid.format(endid[0])
                    cur.execute(sql)
                    results5 = cur.fetchall()
                    if results5 != None and len(results5) > 0:
                        for r5 in results5:
                            common_results.append((tp[0], tp[1], tp[2], tp[3], tp[4], tp[5], tp[6],tp[7],tp[8], r5[0], endid[0]))
                    else:
                        pass
                if common_results != None and len(common_results) > 0:  # find 4
                    cresults = []
                    for comr in common_results:
                        cur.execute(sql_find_namebyaid.format(comr[0]))
                        actor1 = cur.fetchone()
                        cur.execute(sql_find_moviebymid.format(comr[1]))
                        movie1 = cur.fetchone()
                        cur.execute(sql_find_namebyaid.format(comr[2]))
                        actor2 = cur.fetchone()
                        cur.execute(sql_find_moviebymid.format(comr[3]))
                        movie2 = cur.fetchone()
                        cur.execute(sql_find_namebyaid.format(comr[4]))
                        actor3 = cur.fetchone()
                        cur.execute(sql_find_moviebymid.format(comr[5]))
                        movie3 = cur.fetchone()
                        cur.execute(sql_find_namebyaid.format(comr[6]))
                        actor4 = cur.fetchone()
                        cur.execute(sql_find_moviebymid.format(comr[7]))
                        movie4 = cur.fetchone()
                        cur.execute(sql_find_namebyaid.format(comr[8]))
                        actor5 = cur.fetchone()
                        cur.execute(sql_find_moviebymid.format(comr[9]))
                        movie5 = cur.fetchone()
                        cur.execute(sql_find_namebyaid.format(comr[10]))
                        actor6 = cur.fetchone()
                        cresults.append(
                            actor1[0] + wasinmovie + movie1[0] + " (" + str(movie1[1]) + ") " + withactor + actor2[
                                0] + "; " +
                            actor2[0] + wasinmovie + movie2[0] + " (" + str(movie2[1]) + ") " + withactor + actor3[
                                0] + "; " +
                            actor3[0] + wasinmovie + movie3[0] + " (" + str(movie3[1]) + ") " + withactor + actor4[
                                0] + "; " +
                            actor4[0] + wasinmovie + movie4[0] + " (" + str(movie4[1]) + ") " + withactor + actor5[0]+"; "+
                            actor5[0]+ wasinmovie+movie5[0]+" ("+str(movie5[1])+") "+withactor+actor6[0])

                    cresults.sort()
                    count = 1
                    for cr in cresults:
                        print(str(count) + ". " + cr)
                        count += 1


con.close()

# param_actor1 = sys.argv[1].lower()  # actor 1 name
# param_actor2 = sys.argv[2].lower()  # actor 2 name
#
# if len(param_actor1) == 0 or len(param_actor2) == 0:
#     sys.exit(1)
#
# con = sqlite3.connect('a2.db')
#
# curc = con.cursor()
#
#
# def find_actors(actorid1, movieid):
#     actorids = []
#     find_actors = "select actor_id from acting where movie_id=" + str(movieid) + " and actor_id!=" + str(actorid1)
#     curc.execute(find_actors)
#     tmp_actors = curc.fetchall()
#     if tmp_actors is None or len(tmp_actors) == 0:
#         return None
#     else:
#         for actor in tmp_actors:
#             actorids.append(actor[0])
#         return actorids
#
#
# def find_movies(actorid):
#     movieids = []
#     find_movies = "select movie_id from acting where actor_id=" + str(actorid)
#     curc.execute(find_movies)
#     tmp_movies = curc.fetchall()
#     if tmp_movies is None or len(tmp_movies) == 0:
#         return None
#     else:
#         for movie in tmp_movies:
#             movieids.append(movie[0])
#         return movieids
#
#
# def find_movies2(actorid, mid):
#     movieids = []
#     find_movies = "select movie_id from acting where actor_id=" + str(actorid) + " and movie_id!=" + str(mid)
#     curc.execute(find_movies)
#     tmp_movies = curc.fetchall()
#     if tmp_movies is None or len(tmp_movies) == 0:
#         return None
#     else:
#         for movie in tmp_movies:
#             movieids.append(movie[0])
#         return movieids
#
#
# def find_movie(mid):
#     sql = "select title, year from movie where id=" + str(mid)
#     curc.execute(sql)
#     result = curc.fetchone()
#     return result
#
#
# def find_actor(aid):
#     sql = "select id, name from actor where id=" + str(aid)
#     curc.execute(sql)
#     result = curc.fetchone()
#     return result
#
#
# def two_degree(mids, aid, target):
#     results = []
#     for mid1 in mids:
#         aids1 = find_actors(aid, mid1)
#         for aid1 in aids1:
#             mids2 = find_movies2(aid1, mid1)
#             if mids2 is None or len(mids2) == 0:
#                 continue
#             else:
#                 for mid2 in mids2:
#                     aids2 = find_actors(aid1, mid2)
#                     for aid2 in aids2:
#                         if aid2 == target:
#                             result = (aid, mid1, aid1, mid2, aid2)
#                             results.append(result)
#     return results
#
#
# def three_degree(mids, aid, target):
#     results = []
#     for mid1 in mids:
#         aids1 = find_actors(aid, mid1)
#         for aid1 in aids1:
#             mids2 = find_movies2(aid1, mid1)
#             if mids2 is None or len(mids2) == 0:
#                 continue
#             else:
#                 for mid2 in mids2:
#                     aids2 = find_actors(aid1, mid2)
#                     for aid2 in aids2:
#                         mids3 = find_movies2(aid2, mid2)
#                         if mids3 is None or len(mids3) == 0:
#                             continue
#                         else:
#                             for mid3 in mids3:
#                                 aids3 = find_actors(aid2, mid3)
#                                 for aid3 in aids3:
#                                     if aid3 == target:
#                                         result = (aid, mid1, aid1, mid2, aid2, mid3, aid3)
#                                         results.append(result)
#     return results
#
#
# def four_degree(mids, aid, target):
#     results = []
#     for mid1 in mids:
#         aids1 = find_actors(aid, mid1)
#         for aid1 in aids1:
#             mids2 = find_movies2(aid1, mid1)
#             if mids2 is None or len(mids2) == 0:
#                 continue
#             else:
#                 for mid2 in mids2:
#                     aids2 = find_actors(aid1, mid2)
#                     for aid2 in aids2:
#                         mids3 = find_movies2(aid2, mid2)
#                         if mids3 is None or len(mids3) == 0:
#                             continue
#                         else:
#                             for mid3 in mids3:
#                                 aids3 = find_actors(aid2, mid3)
#                                 for aid3 in aids3:
#                                     mids4 = find_movies2(aid3, mid3)
#                                     if mids4 is None or len(mids4) == 0:
#                                         continue
#                                     else:
#                                         for mid4 in mids4:
#                                             aids4 = find_actors(aid3, mid4)
#                                             for aid4 in aids4:
#                                                 if aid4 == target:
#                                                     result = (aid, mid1, aid1, mid2, aid2, mid3, aid3, mid4, aid4)
#                                                     results.append(result)
#     return results
#
#
# def five_degree(mids, aid, target):
#     results = []
#     for mid1 in mids:
#         aids1 = find_actors(aid, mid1)
#         for aid1 in aids1:
#             mids2 = find_movies2(aid1, mid1)
#             if mids2 is None or len(mids2) == 0:
#                 continue
#             else:
#                 for mid2 in mids2:
#                     aids2 = find_actors(aid1, mid2)
#                     for aid2 in aids2:
#                         mids3 = find_movies2(aid2, mid2)
#                         if mids3 is None or len(mids3) == 0:
#                             continue
#                         else:
#                             for mid3 in mids3:
#                                 aids3 = find_actors(aid2, mid3)
#                                 for aid3 in aids3:
#                                     mids4 = find_movies2(aid3, mid3)
#                                     if mids4 is None or len(mids4) == 0:
#                                         continue
#                                     else:
#                                         for mid4 in mids4:
#                                             aids4 = find_actors(aid3, mid4)
#                                             for aid4 in aids4:
#                                                 mids5 = find_movies2(aid4, mid4)
#                                                 if mids5 is None or len(mids5) == 0:
#                                                     continue
#                                                 else:
#                                                     for mid5 in mids5:
#                                                         aids5 = find_actors(aid4, mid5)
#                                                         for aid5 in aids5:
#                                                             if aid5 == target:
#                                                                 result = (
#                                                                     aid, mid1, aid1, mid2, aid2, mid3, aid3, mid4, aid4,
#                                                                     mid5, aid5)
#                                                                 results.append(result)
#     return results
#
#
# def six_degree(mids, aid, target):
#     results = []
#     for mid1 in mids:
#         aids1 = find_actors(aid, mid1)
#         for aid1 in aids1:
#             mids2 = find_movies2(aid1, mid1)
#             if mids2 is None or len(mids2) == 0:
#                 continue
#             else:
#                 for mid2 in mids2:
#                     aids2 = find_actors(aid1, mid2)
#                     for aid2 in aids2:
#                         mids3 = find_movies2(aid2, mid2)
#                         if mids3 is None or len(mids3) == 0:
#                             continue
#                         else:
#                             for mid3 in mids3:
#                                 aids3 = find_actors(aid2, mid3)
#                                 for aid3 in aids3:
#                                     mids4 = find_movies2(aid3, mid3)
#                                     if mids4 is None or len(mids4) == 0:
#                                         continue
#                                     else:
#                                         for mid4 in mids4:
#                                             aids4 = find_actors(aid3, mid4)
#                                             for aid4 in aids4:
#                                                 mids5 = find_movies2(aid4, mid4)
#                                                 if mids5 is None or len(mids5) == 0:
#                                                     continue
#                                                 else:
#                                                     for mid5 in mids5:
#                                                         aids5 = find_actors(aid4, mid5)
#                                                         for aid5 in aids5:
#                                                             mids6 = find_movies2(aid5, mid5)
#                                                             if mids6 is None or len(mids6) == 0:
#                                                                 continue
#                                                             else:
#                                                                 for mid6 in mids6:
#                                                                     aids6 = find_actors(aid5, mid6)
#                                                                     for aid6 in aids6:
#                                                                         if aid6 == target:
#                                                                             result = (
#                                                                             aid, mid1, aid1, mid2, aid2, mid3, aid3,
#                                                                             mid4, aid4, mid5, aid5, mid6, aid6)
#                                                                             results.append(result)
#                                                                         else:
#                                                                             pass
#     return results
#
#
# #############################################################
# cur_actor = con.cursor()
# sql_actor1 = "select id, name from actor where lower(name)=" + "'" + param_actor1 + "'"
# sql_actor2 = "select id, name from actor where lower(name)=" + "'" + param_actor2 + "'"
# # print(sql_actor1)
# # print(sql_actor2)
#
# # find actor1 and actor2 (id, name)
# cur_actor.execute(sql_actor1)
# actor1 = cur_actor.fetchone()
# if actor1 is None or len(actor1) == 0:
#     sys.exit(1)
# cur_actor.execute(sql_actor2)
#
# actor2 = cur_actor.fetchone()
# if actor2 is None or len(actor2) == 0:
#     sys.exit(1)
#
# # print(actor1)
# # print(actor2)
#
# ##############################################################
#
# results = []
# was_in = " was in "
# withs = " with "
#
# cur = con.cursor()
#
# sql_actor_query = "select movie_id from acting join actor on acting.actor_id=actor.id where lower(actor.name)="
# sql_inter = " intersect "
#
# sql = sql_actor_query + "'" + param_actor1 + "'"
# cur.execute(sql)
# movies = cur.fetchall()
# if movies is None:
#     sys.exit(1)
# sql = sql_actor_query + "'" + param_actor2 + "'"
#
# cur.execute(sql)
# movies = cur.fetchall()
# if movies is None:
#     sys.exit(1)
#
# sql = sql_actor_query + "'" + param_actor1 + "'" + sql_inter + sql_actor_query + "'" + param_actor2 + "'"
# # print(sql)
#
# cur.execute(sql)
# movies = cur.fetchall()
#
# if movies is not None and len(movies) > 0:
#     movieids = []
#     for movie in movies:
#         movieids.append(movie[0])
#     sql_query = "select title, year from movie where id = "
#
#     for movie_id in movieids:
#         cur.execute(sql_query + str(movie_id))
#         one_degree = cur.fetchone()
#         result = actor1[1] + was_in + one_degree[0] + " (" + str(one_degree[1]) + ") " + withs + actor2[1]
#         results.append(result)
#
#     results.sort()
#     index = 1
#     for r in results:
#         print(str(index) + ".", r)
#         index += 1
# else:  # not one degree
#     sql = sql_actor_query + "'" + param_actor1 + "'"
#     cur.execute(sql)
#     movies = cur.fetchall()
#     movieids = []
#     for movie in movies:
#         movieids.append(movie[0])
#     # print(movieids)
#
#     two_degrees = two_degree(movieids, actor1[0], actor2[0])
#     # print(two_degrees)
#     results = []
#     if two_degrees is not None and len(two_degrees) > 0:
#         for t in two_degrees:
#             movie1 = find_movie(t[1])
#             movie2 = find_movie(t[3])
#             results.append(
#                 find_actor(t[0])[1] + was_in + movie1[0] + " (" + str(movie1[1]) + ") " + withs + find_actor(t[2])[
#                     1] + "; " + find_actor(t[2])[1] + was_in + movie2[0] + " (" + str(movie2[1]) + ") " + withs +
#                 find_actor(t[4])[1])
#         results.sort()
#
#         index = 1
#         for r in results:
#             print(str(index) + ".", r)
#             index += 1
#
#     else:  # not two degree
#         three_degrees = three_degree(movieids, actor1[0], actor2[0])
#         if three_degrees is not None and len(three_degrees) > 0:
#             for t in three_degrees:
#                 movie1 = find_movie(t[1])
#                 movie2 = find_movie(t[3])
#                 movie3 = find_movie(t[5])
#                 results.append(
#                 find_actor(t[0])[1] + was_in + movie1[0] + " (" + str(movie1[1]) + ") " + withs + find_actor(t[2])[1] + "; "
#                 + find_actor(t[2])[1] + was_in + movie2[0] + " (" + str(movie2[1]) + ") " + withs +find_actor(t[4])[1] + "; "
#                 + find_actor(t[4])[1]+ was_in +movie3[0]+" ("+str(movie3[1])+") "+ withs +find_actor(t[6])[1]
#                 )
#             results.sort()
#
#             index = 1
#             for r in results:
#                 print(str(index) + ".", r)
#                 index += 1
#         else:
#             four_degrees = four_degree(movieids, actor1[0], actor2[0])
#             if four_degrees is not None and len(four_degrees) > 0:
#                 for t in four_degrees:
#                     movie1 = find_movie(t[1])
#                     movie2 = find_movie(t[3])
#                     movie3 = find_movie(t[5])
#                     movie4= find_movie(t[7])
#                     results.append(
#                         find_actor(t[0])[1] + was_in + movie1[0] + " (" + str(movie1[1]) + ") " + withs +
#                         find_actor(t[2])[1] + "; "
#                         + find_actor(t[2])[1] + was_in + movie2[0] + " (" + str(movie2[1]) + ") " + withs +
#                         find_actor(t[4])[1] + "; "
#                         + find_actor(t[4])[1] + was_in + movie3[0] + " (" + str(movie3[1]) + ") " + withs +
#                         find_actor(t[6])[1] +"; "
#                         +find_actor(t[6])[1] + was_in + movie4[0] + " (" + str(movie4[1]) + ") " + withs +
#                         find_actor(t[8])[1]
#                     )
#                 results.sort()
#
#                 index = 1
#                 for r in results:
#                     print(str(index) + ".", r)
#                     index += 1
#             else:
#                 five_degrees = five_degree(movieids, actor1[0], actor2[0])
#                 # print(five_degrees)
#                 # for t in five_degrees:
#                 #     print(t)
#                 if five_degrees is not None and len(five_degrees) > 0:
#                     for t in five_degrees:
#                         movie1 = find_movie(t[1])
#                         movie2 = find_movie(t[3])
#                         movie3 = find_movie(t[5])
#                         movie4 = find_movie(t[7])
#                         movie5 = find_movie(t[9])
#                         results.append(
#                             find_actor(t[0])[1] + was_in + movie1[0] + " (" + str(movie1[1]) + ") " + withs +
#                             find_actor(t[2])[1] + "; "
#                             + find_actor(t[2])[1] + was_in + movie2[0] + " (" + str(movie2[1]) + ") " + withs +
#                             find_actor(t[4])[1] + "; "
#                             + find_actor(t[4])[1] + was_in + movie3[0] + " (" + str(movie3[1]) + ") " + withs +
#                             find_actor(t[6])[1] + "; "
#                             + find_actor(t[6])[1] + was_in + movie4[0] + " (" + str(movie4[1]) + ") " + withs +
#                             find_actor(t[8])[1]+"; "
#                             + find_actor(t[8])[1] + was_in + movie5[0] + " (" + str(movie5[1]) + ") " + withs +
#                             find_actor(t[10])[1]
#                         )
#                     results.sort()
#
#                     index = 1
#                     for r in results:
#                         print(str(index) + ".", r)
#                         index += 1
#
