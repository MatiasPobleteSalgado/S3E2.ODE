#include <SDL2/SDL.h>
#include <cuda.h>
#include <math.h>
#include <stdlib.h>
#include "kernels.cu"
#include "schoolData.cpp"
#include <vector>
#include <cxxopts.hpp>

using namespace std;

int main (int argc, char** argv){
    /*
    cxxopts::Options options("MyProgram", "One line description of MyProgram");
    options.add_options(
        ("g,gui", "Enable use interface")
    );
    bool gui = false;
    try{
        auto result = options.parse(argc, argv);
        bool gui = result["gui"].as<bool>();
    }
    catch(cxxopts::OptionSpecException e){
        printf("Spec %s \n", e.what());
        return 1;
    }
    catch(cxxopts::OptionParseException e){
        printf("Parse %s \n", e.what());
        return 1;
    }
    */

    bool gui = false;
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
    float *u1, *u2, *u3, *v1, *v2, *c1, *c2, *m1, *m2;
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
    
    cudaMallocManaged(&m1, 3 * sizeof(float));
    cudaMallocManaged(&m2, 3 * sizeof(float));

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
    c1[0] = -1.0f;
    c1[1] = 0.0f;
    c1[2] = 1.0f;

    c2[0] = 1.0f;
    c2[1] = 0.0f;
    c2[2] = -1.0f;

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
        // Verify used space
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

    /*
    s[0] = 2;
    s[105000] = 1;
    s[105000 + 1024 * 100] = 3;
    s[105000 + 1024 * 50 + 20] = 4;
    s[105000 + 1024 * 50 + -20] = 5;
    */
    SDL_Window *scr1 = NULL;
    SDL_Renderer *renderer1 = NULL;
    SDL_Event e1;
    SDL_Rect renderer1_viewport;
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
        renderer1_viewport = {0, 0 , 1024, 1024};
        SDL_RenderSetViewport(renderer1, &renderer1_viewport);
	    // Window variables
        /*
	    scr2 = SDL_CreateWindow (
	        "Student Simulation", 
	        SDL_WINDOWPOS_UNDEFINED,
	        SDL_WINDOWPOS_UNDEFINED,
	        nX,
	        nY,
	        SDL_WINDOW_SHOWN
	    );
	    renderer2 = SDL_CreateRenderer(scr2, -1, SDL_RENDERER_ACCELERATED);
        */
    }
    float zoom = 1.0f;
    int nx = 0, ny = 0; 
    int iterations = 0;
    int max_iterations = 1000000; 
    while(iteracions < max_iterations){
        iterations++;
        /*
        printf(
            "v1: up=%f down=%f \nv2: up=%f down=%f \n", 
            v1[105000 + 1], 
            v1[105000 + 1024 * 100 + 1],
            v2[105000 - 1], 
            v2[105000 + 1024 * 100 - 1]
        );
        */
        updateU<<<nX, nY>>>(cells, u1, 1, s, 10.0, nX, nY, 0.1);
        updateU<<<nX, nY>>>(cells, u2, 2, s, 10.0, nX, nY, 0.1);
        updateU<<<nX, nY>>>(cells, u3, 3, s, 10.0, nX, nY, 0.1);
        cudaDeviceSynchronize();

        updateV<<<nX, nY>>>(cells, u1, u2, u3, v1, 4, s, c1, m1, nX, nY, 0.1);
        updateV<<<nX, nY>>>(cells, u1, u2, u3, v2, 5, s, c2, m2, nX, nY, 0.1);
        cudaDeviceSynchronize();

        if(gui){
		    SDL_SetRenderDrawColor(renderer1, 0, 0, 0, 255);
	    	SDL_RenderClear(renderer1);
	        while( SDL_PollEvent( &e1 ) != 0 ){
	            switch(e1.type){
                    case SDL_QUIT:
                        on = false;
                        break;
                    case SDL_MOUSEBUTTONDOWN:
                        switch(e1.button.button){
                            case SDL_BUTTON_LEFT:
                                zoom += 0.05;
                            break;
                            case SDL_BUTTON_RIGHT:
                                zoom -= 0.05;
                                if(zoom < 1){
                                    zoom = 1;
                                }
                            break;
                        }

                    break;
                }
	        }
            SDL_GetMouseState(&nx, &ny);
            renderer1_viewport.w = 1024 * zoom;
            renderer1_viewport.h = 1024 * zoom;
            renderer1_viewport.x = nx - renderer1_viewport.w / 2;
            renderer1_viewport.y = ny - renderer1_viewport.w / 2;
            SDL_RenderSetViewport(renderer1, &renderer1_viewport);
	        int x = 0, y = 0;
		    for(int i = 0; i < cellIndx; i++){
		    	if(x < (nX -1)){
		    		x++;
		    	}
		    	else{
		    		x = 0;
		    		y++;
		    	}
                /*
                SDL_SetRenderDrawColor(
                    renderer1, 
                    (u1[i] / MAX * 255) + (v1[i] / MAX * 255) + (v2[i] / MAX * 255), 
                    (u2[i] / MAX * 255) + (v2[i] / MAX * 255) + (v1[i] / MAX * 255), 
                    (u3[i] / MAX * 255) + (v1[i] / MAX * 255), 255
                );
                */
                SDL_SetRenderDrawColor(
                    renderer1, 
                    (u1[i] + v1[i]) / MAX * 255, 
                    (u2[i] + (v1[i] + v2[i]) * 0.5) / MAX * 255, 
                    (u3[i] + v2[i]) / MAX * 255, 
                    255
                );
                SDL_RenderDrawPoint(renderer1, x * zoom, y * zoom);

                /*
	            SDL_SetRenderDrawColor(renderer1, v1[i] / MAX * 255, 0, v2[i] / MAX * 255, 255);
		    	SDL_RenderDrawPoint(renderer1, x, y);
                */
		    }
		    SDL_RenderPresent(renderer1);
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
    SDL_Quit();

    return EXIT_SUCCESS;
}