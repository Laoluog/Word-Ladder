import math
from Graph import Graph
from valid_ladders_word_list import get_valid_word_list

class LadderGraph(Graph):
    def __init__(self, word_list:list[str]):
        adj_list = self.build_adj_list(word_list)
        super().__init__(adj_list)

    def hamming_distance(self, w1:str, w2:str)-> int:
        '''Determines the hamming distance between two words
        '''
        count = 0
        for x in range(len(w1)):
            if w1[x] != w2[x]:
                count+=1
        return count


    def build_adj_list(self, word_list: list[str])-> dict[str, set[str]]:
        '''Builds an adjacency list modeling a graph where nodes are all words
           with the same length, and edges connect words that differ by exactly 1 letter
        '''
        di = {}
        for x in word_list:
           di[x.lower()] = set()
        for x in range(len(word_list)):
          word_list[x] = word_list[x].lower()
          for y in range(x+1,len(word_list)):
            word_list[y]=word_list[y].lower()
            if self.hamming_distance(word_list[x],word_list[y]) == 1:
              di[word_list[x]].add(word_list[y])
              di[word_list[y]].add(word_list[x])
        return(di) 
   
    def is_valid_word(self, word:str) -> bool:
        '''Determines whether a word is present in the graph
        '''       
        word = word.lower()
        return super().is_vertex(word)


    def is_valid_ladder(self, ladder:tuple[str]) -> bool:
       ''' Determines whether a given ladder is a valid path on the graph
       '''
       li = []

       
       for x in range(len(ladder)):
          li.append(ladder[x].lower())
       li = tuple(li)
       if str(li)[-2:] == ",)":
          return False

       return super().is_valid_path(li)

    def get_rung_length(self, ladder:tuple[str]) -> int:
        ''' Finds the number of rungs in the word ladder.
        '''

        if not self.is_valid_ladder(ladder):
           return -1
        
        counter = 0
        for x in ladder:
           counter +=1
        return counter-2
 
    def get_shortest_ladder(self, start:str, target:str) -> tuple[str]:
        '''Finds a shortest ladder connecting the start vertex with the target vertex.
        '''
        
        return super().get_shortest_bfs_path(start.lower(), target.lower())


    def get_all_shortest_ladders(self, start:str, target:str) -> set[tuple[str]]:
        ''' Finds all of the shortests ladders connecting the start vertex with the target vertex.
        '''

        return super().get_all_shortest_bfs_paths(start.lower(), target.lower())

    
    def get_all_ladders(self, start:str, target:str, max_rungs=math.inf) -> set[tuple[str]]:
        ''' Finds all of the shortests paths connecting the start vertex with the target vertex.
        '''
        length = max_rungs
        if length == 0:
           return set()
        length+=2
        print("THIS IS THE LENGTH", length)
        path_queue = [[start]]
          
        
        s = set()
        while path_queue:
            old_path = path_queue.pop(0)
            if len(old_path) > length+1:
               return s
            last_node = old_path[-1]

            for neighbour in sorted(super().get_neighbors(last_node)):
                if neighbour not in old_path:
                    new_path = old_path.copy()
                    new_path.append(neighbour)
                    path_queue.append(new_path)

                    if len(new_path) <= length and neighbour == target:
                      s.add(tuple(new_path))

            if len(path_queue) == 0:
              return s

if __name__ == "__main__":
  small_dictionary=["foul","fool","cool","pool","poll","pole","pope","pale","sale", "sage", "page", "pall", "fall", "fail", "foil"]
  myLadderGraph = LadderGraph(small_dictionary)
  
  print("Vertices:", myLadderGraph.vertices)
  print("Edges:", myLadderGraph.edges)  
  print()

  valid_vertex = "foil"
  invalid_vertex = "ffff"
  print(f"Neighbers ({valid_vertex}):", myLadderGraph.get_neighbors(valid_vertex))
  print(f"Valid word ({valid_vertex}):", myLadderGraph.is_valid_word(valid_vertex))
  print(f"Invalid word ({invalid_vertex}):", myLadderGraph.is_valid_word(invalid_vertex))
  print()

  good_ladder=('fool', 'pool', 'poll', 'pall', 'pale', 'page', 'sage')
  bad_ladder=('fool', 'pool', 'pall', 'pale', 'page', 'sage')
  laddy = ('fool',)
  print(f"Valid Path {laddy}:", myLadderGraph.is_valid_ladder(laddy))
  print(f"Valid Path Rung Length {good_ladder}:", myLadderGraph.get_rung_length(good_ladder))
  print(f"Invalid Path {bad_ladder}:", myLadderGraph.is_valid_ladder(bad_ladder))
  print(f"Invalid Path Rung Length {bad_ladder}:", myLadderGraph.get_rung_length(bad_ladder))
  print()
  
  start = "foul"
  target= "sage"
  print(f"Shortest ladder from {start} to {target}", myLadderGraph.get_shortest_ladder(start, target))
  print()
  all_shortest_ladders = myLadderGraph.get_all_shortest_ladders(start, target)
  print(f"All {len(all_shortest_ladders)} Shortest Ladders from {start} to {target}", all_shortest_ladders)
  print()
  max_rung_length = 6
  all_ladders = myLadderGraph.get_all_ladders(start, target, max_rung_length )
  print(f"All {len(all_ladders)} Ladders with a max length of {max_rung_length} from {start} to {target}", all_ladders)