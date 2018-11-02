"""
1st: set levels (if levels == 1, then only macro--tetrahedra)

searching repeated vertices:
take from second column in file elem_by_vert.txt because 6,5 y 4 are not 
things to replace. the analogue for faces repetitions
another option is to put -3 -2 y -1 etc ...

Obs: write_elements_by_vertices_T4() has 4*ones 
has to be changed to: -np.ones( whatever , dtype=int) etc
"""
import numpy as np
import mesh
import mesh_write
import mesh_conectivity
import time

#print (time.time())
## macro_elements type 1: prisms, pyrs and tetra
## macro_elements type 2: prisms
## macro_elements type 3: tetra

tTot 		 = time.time()
levels 		 = 3
n_vert_prism = 6
print('levels: %s\r' % levels)

mu_ 		= .35
p_ 			= np.array([[ 1,  1,  1,  1,  0,  0,  0,  0], 	# octant 8
       					[-1,  0,  0, -1, -1,  0,  0, -1],   # x > 0, y < 0, z < 0
       					[-1, -1,  0,  0, -1, -1,  0,  0]])
## organization of the 5 tetrahedra resolving a cube: 
## the vertices of the macro--cube are: 0 ... 7.
macro_el 	= np.array([[0,1,3,4],[2,3,1,6],[7,3,4,6],[5,4,1,6],[6,1,3,4]])

## dictionary with the fichera mesh.
print 'mesh.cube_mesh_2()'
t0 = time.time()
fichera_coords_ = mesh.cube_mesh_2(levels, mu_, p_, macro_el) 
print time.time() - t0
print '\r'

# indices only for type I macro--el. writes file: elements.txt 
mesh_write.write_element_indices('elements.txt', levels)

init 	= 0

for oc in xrange(2,9):    # integers 2, 3, 4, 5, 6, 7, 8
	for t in xrange(4):
		coords 	= fichera_coords_['points_T' + str(t) + '_C' + str(oc)] 
		mesh_conectivity.write_elements_by_vertices('elements.txt', levels, 'Octave', init) # writes elements_by_vertices_repeated.txt: GLOBAL INDICES per element
		init   += mesh_write.vertices(coords)	# writes 'vertices.txt' global list of vertices
	## Type II macro--element
	n_vertT4 = mesh.np.shape(fichera_coords_['points_T4_C' + str(oc)])[0]

	if not ((n_vertT4 % 4) == 0):
		print('incorrect number of points in T4')
		print('oc:' + str(oc) + ' t:' + str(t))
		exit()

	mesh_conectivity.write_elements_by_vertices_T4(n_vertT4, init ,'elements_by_vertices_repeated.txt')
	init += mesh_write.verticesT4(fichera_coords_['points_T4_C' + str(oc)], 'vertices.txt')

## look for repetitions of vertices
with open('elements_by_vertices_repeated.txt','r') as inp:
	things = inp.readlines()

n_elem = len(things)

elem_vert_repeated = mesh.np.zeros((n_elem,n_vert_prism+1),dtype=int)
for k in range(len(things)):
	ele 					= mesh.np.fromstring(things[k],dtype=int,sep=' ')
	elem_vert_repeated[k] 	= mesh.np.concatenate((ele,mesh.np.zeros((n_vert_prism+1-len(ele)),dtype=int)))

print 'mesh_conectivity.kill_repeated()'
t0 = time.time()
replace_verts = mesh_conectivity.kill_repeated('vertices.txt')  ## repetitions in vertices.txt leave a dictionary
print time.time() - t0
print '\n'

print 'vertices replacement loop version 2'
t0 		= time.time()
counter = 1
elem_vert_dscnt_indcs = mesh.np.copy(elem_vert_repeated).reshape(n_elem*7)
for key in replace_verts:
	print 'progress: {0}/{1}\r'.format(counter,len(replace_verts)),
	counter += 1
	for r in replace_verts[key]:
		elem_vert_dscnt_indcs[elem_vert_dscnt_indcs == r+1] = (key +1)
print '\r'
print time.time() - t0
print '\n'

elem_vert_dscnt_indcs = elem_vert_dscnt_indcs.reshape((n_elem,7))

del elem_vert_repeated

## <--- whithout repetitions
with open('elements_by_vertices.txt','w') as out:
	for e in elem_vert_dscnt_indcs:
		mesh.np.savetxt(out, e[0:e[0]+1].reshape((1,e[0]+1)), fmt='%d')

"""
##############################################################################
# at this point the program is already general:
# this 'inverts' the table of elements_by_vertices.txt
# writes on disc: vertices_by_elements.txt
mesh_conectivity.vertices_by_elements('elements_by_vertices.txt', 'Octave')
##############################################################################
"""

"""
##############################################################################
# general function. 
# takes output of mesh_conectivity.vertices_by_elements()
# writes on disc: shared_faces.txt
####### SLOW (not used for now)
print('mesh_conectivity.faces()')
print(time.time())
d = mesh_conectivity.faces('vertices_by_elements.txt', n_elem, 'Octave')
print(time.time())
print('\n')
##############################################################################
"""

# writes files: faces_repeated.txt 			----> with repetitions
#               faces_local_to_global.txt   ----> for macro--element of type 1
print 'mesh_conectivity.face_enumeration'
t0 = time.time()
mesh_conectivity.face_enumeration('elements_by_vertices.txt')
print time.time() - t0
print '\r'

with open('faces_local_to_global.txt', 'r') as ent:
	stuff = ent.readlines()

elem_faces_repeated = mesh.np.zeros((n_elem, 6),dtype=int)
for elem in range(len(stuff)):
	el 							= mesh.np.fromstring(stuff[elem],dtype=int,sep=' ')
	elem_faces_repeated[elem] 	= mesh.np.concatenate((el,mesh.np.zeros((6-len(el)),dtype=int)))

## reads repetitions in faces_repeated.txt and leaves a dictionary
## writes file: faces.txt                  -----> global unique enumeration of faces
print 'mesh_conectivity.kill_repeated_faces'
t0 = time.time()
replace_faces, indices, num_faces = mesh_conectivity.kill_repeated_faces('faces_repeated.txt')  
print time.time() - t0
print '\r'

with open ('num_faces.txt','w') as n_of_faces:
	n_of_faces.write(str(num_faces))

#### uniquifying faces:
print 'faces replacement loop version 2'
t0 = time.time()
elem_faces_discnt_index = mesh.np.copy(elem_faces_repeated).reshape(n_elem*6)
counter = 1
for key in replace_faces:
	print 'progress: {0}/{1}\r'.format(counter,len(replace_faces)),
	counter += 1
	for r in replace_faces[key]:
		elem_faces_discnt_index[elem_faces_discnt_index==r] = key
print '\r'
print time.time() - t0
print '\r'

#elem_faces_discnt_index = elem_faces_discnt_index.reshape((n_elem,6))

del elem_faces_repeated

## bijection indices ----> [1,...,n_faces]
## unique, continuous indices with filling zeros
print 'loop for indexing faces with {1 ... n_faces}'
t0 = time.time()
elem_faces = mesh.np.copy(elem_faces_discnt_index)
for i in range(len(indices)):
	elem_faces[elem_faces_discnt_index==indices[i]] = i+1
print time.time() - t0
print '\r'

elem_faces = mesh.np.copy(elem_faces).reshape((n_elem,6))
del elem_faces_discnt_index

with open('elements_by_faces.txt','a') as ex:
	for elem in elem_faces:
		mesh.np.savetxt(ex, elem.reshape((1,6)),fmt='%d')

print 'Total time'
print(time.time() - tTot)
