#include <SDL2/SDL.h>
#include <cuda.h>
#include <math.h>
#include <stdlib.h>
#include "kernels.cu"
#include "schoolData.cpp"
#include <vector>

using namespace std;

int main (int argc, char** argv){
	bool gui = true;
	bool on = true;
	srand(time(NULL));
	// Model definition
    double dimX = 2048, dimY = 2048;
    int nX = 1024, nY = 1024, cellIndx = 0, scale = 1, MAX = 1000;
    /*
	The five diffusion variables and "attraction" coeficients
	on unified memory
	The s variable in the future can represent features of the space
	like streets. Now it represents the exact position of schools and students
	and their type so the GPU can use that information
    */
    SDL_Rect *cells; // Rectangular info {x, y, width, height} 
    float *u1, *u2, *u3, *v1, *v2, *c1, *c2;
    int *s;
    cudaMallocManaged(&cells, nX * nY * sizeof(SDL_Rect));
    cudaMallocManaged(&u1, nX * nY * sizeof(float));
    cudaMallocManaged(&u2, nX * nY * sizeof(float));
    cudaMallocManaged(&u3, nX * nY * sizeof(float));
    cudaMallocManaged(&v1, nX * nY * sizeof(float));
    cudaMallocManaged(&v2, nX * nY * sizeof(float));
    cudaMallocManaged(&s,  nX * nY * sizeof(int));
    cudaMallocManaged(&c1, 3 * sizeof(float));
    cudaMallocManaged(&c2, 3 * sizeof(float));

    // Just assure that all memory is clean
    cudaMemset(u1, 0, nX * nY * sizeof(float));
    cudaMemset(u2, 0, nX * nY * sizeof(float));
    cudaMemset(u3, 0, nX * nY * sizeof(float));
    cudaMemset(v1, 0, nX * nY * sizeof(float));
    cudaMemset(v2, 0, nX * nY * sizeof(float));
    cudaMemset(s,  0, nX * nY * sizeof(int));
    cudaMemset(c1, 0, 3 * sizeof(float));
    cudaMemset(c2, 0, 3 * sizeof(float));

    // Set coef values
    c1[0] = 0.5f;
    c1[1] = 0.4f; 
    c1[2] = -0.2f; 

    c2[0] = -0.1f; 
    c2[1] = 0.6f; 
    c2[2] = 0.8f; 

    // Generate grid according to desired values
    for(int y = 0; y < nY; y++){
    	for(int x = 0; x < nX; x++){
    		cells[cellIndx].x = x * (dimX / nX) * scale;
    		cells[cellIndx].y = y * (dimY / nY) * scale;
    		cells[cellIndx].w = dimX / nX * scale;
    		cells[cellIndx].h = dimY / nY * scale;
    		cellIndx++;
    	}
    }

    // Read Shool data from binary file
    vector<School> schools = getShools("schoolData.bin");
    // Populate s array with school types 
    for(auto e: schools){
	    int ex = e.x * nX;
		int ey = nY - (e.y * nY);
		int indx = nX * ey + ex;
		if(s[indx] == 0){
			s[indx] = e.type;
		}
		else{
			s[indx + 1] = e.type;
		}
    }

    for(int i = 0; i < 200; i++){
    	s[rand() % (nX * nY)] = 4;
    }
    for(int i = 0; i < 100; i++){
    	s[rand() % (nX * nY)] = 5;
    }

    SDL_Window *scr1, *scr2 = NULL;
    SDL_Renderer *renderer1, *renderer2 = NULL;
    SDL_Event e1, e2;
    if(gui){
	    // Window variables
	    scr1 = SDL_CreateWindow (
	        "Schools Simulation", 
	        SDL_WINDOWPOS_UNDEFINED,
	        SDL_WINDOWPOS_UNDEFINED,
	        nX,
	        nY,
	        SDL_WINDOW_SHOWN
	    );
	    renderer1 = SDL_CreateRenderer(scr1, -1, SDL_RENDERER_ACCELERATED);
	    // Window variables
	    scr2 = SDL_CreateWindow (
	        "Student Simulation", 
	        SDL_WINDOWPOS_UNDEFINED,
	        SDL_WINDOWPOS_UNDEFINED,
	        nX,
	        nY,
	        SDL_WINDOW_SHOWN
	    );
	    renderer2 = SDL_CreateRenderer(scr2, -1, SDL_RENDERER_ACCELERATED);
    }

    while(on){
        updateU<<<nX, nY>>>(cells, u1, 1, s, 0.25, nX, nY, 1);
        updateU<<<nX, nY>>>(cells, u2, 2, s, 0.5, nX, nY, 1);
        updateU<<<nX, nY>>>(cells, u3, 3, s, 1.0, nX, nY, 1);
        cudaDeviceSynchronize();

        updateV<<<nX, nY>>>(cells, u1, u2, u3, v1, 4, s, c1, nX, nY, 1);
        updateV<<<nX, nY>>>(cells, u1, u2, u3, v2, 5, s, c2, nX, nY, 1);
        cudaDeviceSynchronize();

        if(gui){
		    SDL_SetRenderDrawColor(renderer1, 255, 255, 255, 255);
	    	SDL_RenderClear(renderer1);
		    SDL_SetRenderDrawColor(renderer2, 255, 255, 255, 255);
	    	SDL_RenderClear(renderer2);
	        while( SDL_PollEvent( &e1 ) != 0 ){
	            if( e1.type == SDL_QUIT ){
	                on = false;
	            }
	        }
	        while( SDL_PollEvent( &e2 ) != 0 ){
	            if( e2.type == SDL_QUIT ){
	                on = false;
	            }
	        }
	        int x = 0, y = 0;

		    for(int i = 0; i < cellIndx; i++){
		    	if(x < (nX -1)){
		    		x++;
		    	}
		    	else{
		    		x = 0;
		    		y++;
		    	}
	            SDL_SetRenderDrawColor(renderer1, u1[i] / MAX * 255, u2[i] / MAX * 255, u3[i] / MAX * 255, 255);
		    	SDL_RenderDrawPoint(renderer1, x, y);
		    }
		    x = 0;
		    y = 0;
		    for(int i = 0; i < cellIndx; i++){
		    	if(x < (nX -1)){
		    		x++;
		    	}
		    	else{
		    		x = 0;
		    		y++;
		    	}
	            SDL_SetRenderDrawColor(renderer2, v1[i] / MAX * 255, 0, v2[i] / MAX * 255, 255);
		    	SDL_RenderDrawPoint(renderer2, x, y);
		    }
		    SDL_RenderPresent(renderer1);
		    SDL_RenderPresent(renderer2);
        }
	}

    cudaFree(cells);
    cudaFree(u1);
    cudaFree(u2);
    cudaFree(u3);
    cudaFree(v1);
    cudaFree(v2);
    cudaFree(c1);
    cudaFree(c2);
    cudaFree(s);

    SDL_DestroyWindow(scr1);
    SDL_DestroyWindow(scr2);
    SDL_Quit();

    return EXIT_SUCCESS;
}