def contour():
  #int vert_idx = 1;
  vert_idx = 1
  #FILE *ours = fopen(outname, "w");
  #for (int I = 0; I < size[0] - 1; I++)
  #{
  for I in range(0,size[0] - 1):
    #for (int J = 0; J < size[1] - 1; J++)
    #{
    for J in range(0,size[1] - 1):
      #for (int K = 0; K < size[2] - 1; K++)
      #{
      for K in range(0,size[2] - 1):
          #// get index
      	  #int idx = 0;
          idx = 0
	  #for (int k = 0, m = 0; k < 2; k++)
          #  for (int j = 0; j < 2; j++)
	  #     for (int i = 0; i < 2; i++, m++)
		   #idx |= get_thresh(I+i,J+j,K+k) << m;
          m=0
	  for k in range(0,2):
            for j in range(0,2):
              for i in range(0,2):
		  idx |= get_thresh(I+i,J+j,K+k) << m;
                  m=m+1

	  #for (int i = 0; mc_cycle_table[idx][i][0] >= 0; i++)
	  #{
          i=0
          while  mc_cycle_table[idx][i][0] >= 0 #; i++)
            #// calc verts
	    #BoundedArray<int, 8> verts;
            verts=[]
	    #for (int j = 0; mc_cycle_table[idx][i][j] >= 0; j++)
	    #{
            j=0
            while mc_cycle_table[idx][i][j] >= 0# ; j++)
              #int e0,e1;
              #float v0,v1;
              #vect3f p0,p1;

	      e0 = cube_edge2vert[mc_cycle_table[idx][i][j]][0];
	      e1 = cube_edge2vert[mc_cycle_table[idx][i][j]][1];

	      v0 = get_val(I + (e0&1), J + ((e0>>1)&1), K + (e0>>2));
	      v1 = get_val(I + (e1&1), J + ((e1>>1)&1), K + (e1>>2));

	      p0(I + (e0&1), J + ((e0>>1)&1), K + (e0>>2));
	      p1(I + (e1&1), J + ((e1>>1)&1), K + (e1>>2));
	      #float t;
	      #vect3f p;
						
	      #// ours
	      t = lerp(v0, v1);
	      p = p0*(1-t) + p1*t;
	      fprintf(ours, "v %f %f %f\n", p[0]+.5, p[1]+.5, p[2]+.5);

	      #// increment count
	      #verts.push_back(vert_idx++);
              verts.push_back(vert_idx++);
	      

	    #// write tris
	    #for (int j = 2; mc_cycle_table[idx][i][j] >= 0; j++)
	    #{
            j=2
            while mc_cycle_table[idx][i][j] >= 0#; j++)
	      #if (use_flip)
	      #	fprintf(ours, "f %d %d %d\n",verts[0],verts[j],verts[j-1]);
	      #else
	      # fprintf(ours, "f %d %d %d\n",verts[0],verts[j-1],verts[j]);
              fprintf(ours, "f %d %d %d\n",verts[0],verts[j-1],verts[j]);      
	   }
	}
       }
    }
  #fclose(ours);

