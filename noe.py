from numpy import array, sqrt, sum, max, argmax, argmin, arctan2, pi

def createConnectionMat(elems):
  #Find the number of elements
  num_elems = max(elems) + 1
  
  #Create blank connection matrix
  conn = [[] for i in range(num_elems)]
  
  def add_to_conn(i,j):
    if j not in conn[i]:
      conn[i].append(j)
    
  #Populate matrix
  for (a,b,c) in elems:
    add_to_conn(a,b)
    add_to_conn(b,a)
    add_to_conn(a,c)
    add_to_conn(c,a)
    add_to_conn(b,c)
    add_to_conn(c,b)
  
  #Force to tuples
  tuple_conn = [tuple(i) for i in conn]
  return tuple_conn

def findOutline(pts, elems = None):
  #Grab the x and y arrays by themselves
  (x,y) = pts.T
  
  #Grab number of points
  num_pts = pts.shape[0]
  
  #Find one point with the greatest x value
  inx = argmax(x)
  
  #Choose starting direction as downward (there should be no points to the right
  #since this has the greatest x value
  ang = pi/2
  
  #Create output list
  inx_output = [inx]
  
  while (inx not in inx_output[:-1]):
    
    #Grab point
    pt = pts[inx]
    
    #Find all suitable points to grab
    if elems:
      arr_inx = elems[inx]
    else:
      arr_inx = tuple(range(inx)+range(inx+1,num_pts))
    
    srch_pts = pts[arr_inx,:]
    
    #Find the vectors from the current point to all other suitable points
    vecs = [p - pt for p in srch_pts]
    
    #Find the cosines associated with each vector
    angles = [arctan2(y,x) for (x,y) in vecs]
    
    #Post process
    rel_ang = [(a - ang + pi - 1e-8) % (2*pi) for a in angles]
    
    #Find the index of the point with the closest angle to vec
    pt_inx = argmin(rel_ang)
    
    #Find the new vector
    vec = vecs[pt_inx]
    ang = angles[pt_inx]
    
    #Back out the proper index if necessary
    inx = arr_inx[pt_inx]
    
    #Add new point
    inx_output.append(inx)
  
  return inx_output