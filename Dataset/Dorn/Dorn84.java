	float scale_A = (float)hist_size/(max_A-min_A);
	float scale_B = (float)hist_size/(max_B-min_B);

	if(tid < array_size){
		//load array to shared mem and bin it
		s_binned_A[threadIdx.x] = floor( (d_array_A[tid] - min_A) * scale_A );
		s_binned_B[threadIdx.x] = floor( (d_array_B[tid] - min_B) * scale_B );

		if (s_binned_A[threadIdx.x] < 0)
			s_binned_A[threadIdx.x] = 0;
		if (s_binned_B[threadIdx.x] < 0)
			s_binned_B[threadIdx.x] = 0;
		if (s_binned_A[threadIdx.x] >= hist_size)
			s_binned_A[threadIdx.x] = hist_size-1;
		if (s_binned_B[threadIdx.x] >= hist_size)
			s_binned_B[threadIdx.x] = hist_size-1;

		__syncthreads();
	}
	//only one thread writes the results
	if (threadIdx.x == 0)
		for(int i=0;i< blockDim.x; i++)
			if (blockIdx.x*blockDim.x + i < array_size)
				d_joint_hist[ s_binned_A[i] * hist_size + s_binned_B[i] ] ++;
	//d_joint_hist[ s_binned_A[threadIdx.x] * hist_size + s_binned_B[threadIdx.x] ] ++;
	return;  
}



