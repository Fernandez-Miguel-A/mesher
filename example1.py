from mesh import *
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random

def plot_bbrick():
	"""
	TODO: heavily hardcoded just for pyconar. refactor everything
	economizing code
	"""
	mu          = [1,1,1,1,1]#[1,.4,.4,.4,.4]
	macro_elems = [3]  # 0,1,2 or 3 in each cube
	angle_steps = [8,9,10] #range(8,12)
	refinements = range(5,21)
	octants     = [6] # range(6,9) # any sublist in range(2,9)

	permutation_of_vertices = np.array([[0,1,2,3],[3,1,2,0],[3,1,2,0],[0,1,2,3],[0,1,2,3]])
	for n in refinements:
		# here macro_elems is 3, just one hybrid
		coords  = cube_mesh_2(n,mu[3],p_,macro_el,octants,macro_elems)
		drawing = cube_drawing(coords,octants,macro_elems)
	    # drawing = cube_drawing(coords)
		del(coords)
		fig = plt.figure()
		plt.tight_layout()
		ax  = fig.add_subplot(1,1,1, projection='3d')
		
		elev = 30
		
		#for azim in [49, 79,109,139]:
		colors  = ['brown','darkgreen','red','black','fuchsia','blue']*7
		#random.shuffle(colors)
		for azim in angle_steps:
			c   = 0
			# ax.axis('equal')
			# ax.set_xlim3d(0.1,-1.1)
			# ax.set_ylim3d(-1.0,1.0)
			# ax.set_zlim3d(-0.2,1.2)
			ax.view_init(elev, 49 + 15*(azim-1))
			#for tetra in drawing:
			#	col_interval = int(len(tetra)/len(octants))
			#	for o in range(len(octants)):
			#		col = colors[c]
			#		c   = c + 1
			#		for dr in range(col_interval*o, col_interval*(1+o)):
			#			## TODO: this can be done putting (array_of_X, array_of_Y, array_of_Z, ...)
			#			## and not one by one as is now
			#			ax.plot(tetra[dr][0],tetra[dr][1],tetra[dr][2],color = col)
			# now cubic macro-els nr 0,1,2 and 4 with tetrahedra
	        for oc in octants:
	        	for m in [4]:
					q 		= octant(oc, p_)
					P0 	  	= q[:,macro_el[m,permutation_of_vertices[m,0]]]
					P1 	  	= q[:,macro_el[m,permutation_of_vertices[m,1]]]
					P2 	  	= q[:,macro_el[m,permutation_of_vertices[m,2]]]
					P3 	  	= q[:,macro_el[m,permutation_of_vertices[m,3]]]
					points_T5 = macroel_sing_vrtx(P0, P1, P2, P3, mu[m], n)
					for i in [4*nn for nn in range(points_T5.shape[0]/4)]:
						a = np.array([0,1,2,3]+[0,2,3,1])+i*np.ones(8,dtype=int)
					
						b = np.array([2]*8)
						z = points_T5[a,b]
						
						b = np.array([1]*8)
						y = points_T5[a,b]
						
						b = np.array([0]*8)
						x = points_T5[a,b]
						ax.plot(x, y, z)
					del(points_T5)
			# now prismatic macroels
			# TODO
			ax.plot([],[],[],label = "mu[3] = " + str(mu[3]) + " " + str(macro_elems) + " " + str(octants))
			legend = ax.legend()
			ax.set_xlabel(' X ')
			ax.set_ylabel(' Y ')
			ax.set_zlabel(' Z ')
			#plt.show()
            if sys.version_info >= (3, 0):
                print("azim ", azim)
            else:
                print "azim " azim
			fig.savefig('bbrick' + str(azim) + '-' + str(n) + '.png')
	return

def plot_fichera():
	mu          = .5
	macro_elems = [1]  # 0,1,2 or 3 in each cube
	angle_steps = [23]
	refinements = range(4,5)
    if sys.version_info >= (3, 0):
        octants     = list(range(2,3)) # any sublist in range(2,9)
    else:
        octants     = range(2,3) # any sublist in range(2,9)
	
	for n in refinements:
	    coords  = cube_mesh_2(n,mu,p_,macro_el,octants,macro_elems)
	    # uncomment for just the second octant
	    drawing = cube_drawing(coords,octants,macro_elems)
	    # drawing = cube_drawing(coords)
    	
	    fig = plt.figure()
	    elev = 30
    	
	    #for azim in [49, 79,109,139]:
	    colors  = ['brown','darkgreen','red','black','fuchsia','blue']*7
	    #colors  = ['brown','darkgreen','red','black','fuchsia','blue']*7
	    #random.shuffle(colors)
	    for azim in angle_steps:
	        c   = 0
	        ax  = fig.add_subplot(1,1,1, projection='3d')
	        plt.tight_layout()
	        # ax.axis('equal')
	    	# ax.set_xlim3d(0.1,-1.1)
	    	# ax.set_ylim3d(-1.0,1.0)
	    	# ax.set_zlim3d(-0.2,1.2)
	        angle = 49 + 15*(azim-1)
	        ax.view_init(elev, angle)
	        for tetra in drawing:
	            col_interval = int(len(tetra)/len(octants))
	            for o in range(len(octants)):
	                col = colors[c]
	                c   = c + 1
	                for dr in range(col_interval*o, col_interval*(1+o)):
	                    ax.plot(tetra[dr][0],tetra[dr][1],tetra[dr][2],color = col)
	
	        ax.plot([],[],[],label = "mu = " + str(mu) + str(macro_elems) + str(octants))
	        legend = ax.legend()
	        plt.show()
	    plt.close(fig)

plot_fichera()