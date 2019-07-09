#include <vector>

using namespace std;

struct School{
	float x, y;
	int capacity, type;
};

vector<School> getShools(char *path){
	vector<School> schools;
 	School s;
	FILE * fp;
	fp = fopen(path, "rb");
	int cont = 0;
	while(fread(&s, sizeof(School), 1, fp)){
		schools.push_back(s);
		cont++;
	}
	printf("Loaded %d shools \n", cont);
	fclose(fp);
	return schools;
}
