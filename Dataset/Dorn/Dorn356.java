
void et_joint_histogram_gpu(float **d_array_A, float **d_array_B, int **d_jont_hist, int array_size, int hist_size, float min_A, float max_A, float min_B, float max_B)
{
	//CUDA_SAFE_CALL(cudaMemcpyToSymbol(c_backprojection_size,&backprojection_size,sizeof(int3)));
	
	const unsigned int grid = (unsigned int)ceil(array_size/(float)BLOCK);
	dim3 B(BLOCK,1,1);
	dim3 G(grid,1,1);
	
	et_joint_histogram_gpu_kernel <<<G,B>>> (*d_array_A, *d_array_B, *d_jont_hist, array_size, hist_size, min_A, max_A, min_B, max_B);
