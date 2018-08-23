#include <SDL2/SDL.h>
#include <cuda.h>
#include <math.h>
#include <stdlib.h>

__global__ void updateGrid(SDL_Rect * cells, float *temps, int nX, int nY, float dTime){
	//printf("%d\n", cells[threadIdx.x]);
    int num = blockIdx.x *blockDim.x + threadIdx.x;;
    float right, bottom, left, top, temp = temps[num], dTemp;
    int width = cells[num].w, height = cells[num].h;

    printf("%d\n", num);
    if(num < nX){
        if(num == 0){
            right  = temps[num + 1];
            bottom = temps[num + nX];
            dTemp  = (right - temp) / pow(width, 2) + (-temp + bottom) / pow(height, 2);
            temps[num] = temps[num] + dTemp * dTime;
            return;
        }
        if((num + 1) == nX){
            left   = temps[num - 1];
            bottom = temps[num + nX];
            dTemp = (-temp + left) / pow(width, 2) + (-temp + bottom) / pow(height, 2);
            temps[num] = temps[num] + dTemp * dTime;
            return;
        }
        right  = temps[num + 1];
        left   = temps[num - 1];
        bottom = temps[num + nX];
        dTemp  = (right - 2 * temp + left) / pow(width, 2) + (-temp + bottom) / pow(height, 2);
        temps[num] = temps[num] + dTemp * dTime;
        return;
    }
    if((num + 1) > (nY * nX - nX)){
        if((num + 1) == (nY * nX - nX + 1)){
            right  = temps[num + 1];
            top    = temps[num - nX];
            dTemp = (right - temp) / pow(width, 2) + (top - temp) / pow(height, 2);
            temps[num] = temps[num] + dTemp * dTime;
            return;
        }
        if((num + 1) == (nX * nY)){
            top    = temps[num - nX];
            left   = temps[num - 1];
            dTemp = (-temp + left) / pow(width, 2) + (top - temp) / pow(height, 2);
            temps[num] = temps[num] + dTemp * dTime;
            return;
        }
        top    = temps[num - nX];
        left   = temps[num - 1];
        right  = temps[num + 1];
        dTemp = (right - 2 * temp + left) / pow(width, 2) + (top - temp) / pow(height, 2);
        temps[num] = temps[num] + dTemp * dTime;
        return;
    }
    if(((num + 1) % nX) == 1){
        top    = temps[num - nX];
        right  = temps[num + 1];
        bottom = temps[num + nX];
        dTemp = (right - temp) / pow(width, 2) + (top - 2 * temp + bottom) / pow(height, 2);
        temps[num] = temps[num] + dTemp * dTime;
        return;
    }
    if(((num + 1) % nX) == 0){
        left   = temps[num - 1];
        top    = temps[num - nX];
        bottom = temps[num + nX];
        dTemp = (-temp + left) / pow(width, 2) + (top - 2 * temp + bottom) / pow(height, 2);
        temps[num] = temps[num] + dTemp * dTime;
        return;
    }
    right  = temps[num + 1];
    left   = temps[num - 1];
    top    = temps[num - nX];
    bottom = temps[num + nX];
    dTemp = (right - 2 * temp + left) / pow(width, 2) + (top - 2 * temp + bottom) / pow(height, 2);
    temps[num] = temps[num] + dTemp * dTime;
    return;
}

int main (int argc, char** argv){
	// Model definition
    double dimX = 32, dimY = 32;
    int nX = 128, nY = 128, cellIndx = 0, scale = 32;
    SDL_Rect *cells; 
    float *temperatures;
    cudaMallocManaged(&cells, nX * nY * sizeof(SDL_Rect));
    cudaMallocManaged(&temperatures, nX * nY * sizeof(float));

    for(int y = 0; y < nY; y++){
    	for(int x = 0; x < nX; x++){
    		cells[cellIndx].x = x * (dimX / nX) * scale;
    		cells[cellIndx].y = y * (dimY / nY) * scale;
    		cells[cellIndx].w = dimX / nX * scale;
    		cells[cellIndx].h = dimY / nY * scale;
    		cellIndx++;
    	}
    }

    // Window variables
    SDL_Window* scr = NULL;
    bool on = true;
    scr = SDL_CreateWindow (
        "Heat Simulation", 
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        dimX * scale,
        dimY * scale,
        SDL_WINDOW_SHOWN
    );

    SDL_Renderer* renderer = NULL;
    renderer = SDL_CreateRenderer(scr, -1, SDL_RENDERER_ACCELERATED);

    SDL_Event e;
    //temperatures[0] = 1000;
    while(on){
        //   16384
        /*
        temperatures[0] = 1000;
        temperatures[50] = 1000;
        temperatures[500] = 1000;
        temperatures[500] = 1000;
        temperatures[10000] = 1000;
        temperatures[12000] = 1000;
        temperatures[15000] = 1000;
        */
        for(int j = 0; j < 11; j++){
            temperatures[rand() % cellIndx] = 1000;
        }

        //Handle events on queue
        SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
    	SDL_RenderClear(renderer);
        while( SDL_PollEvent( &e ) != 0 ){
            //User requests quit
            if( e.type == SDL_QUIT ){
                on = false;
            }
        }
        updateGrid<<<nX, nY>>>(cells, temperatures, nX, nY, 1);
        cudaDeviceSynchronize();
        // Set render color to blue ( rect will be rendered in this color )
	    // Render rect
	    for(int i = 0; i < cellIndx; i++){
            SDL_SetRenderDrawColor(renderer, temperatures[i] / 1000 * 250, 0, 0, 255 );
	    	SDL_RenderFillRect(renderer, &cells[i]);
	    }
	    SDL_RenderPresent(renderer);
	    // Wait for 5 sec
	    SDL_Delay(16);
    }

    cudaFree(cells);
    cudaFree(temperatures);

    SDL_DestroyWindow(scr);
    SDL_Quit();

    return EXIT_SUCCESS;
}