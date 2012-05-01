gem 'recommendify'
require 'recommendify'
require 'redis'
# Our similarity matrix, we calculate the similarity via co-concurrence 
# of products in "orders" using the jaccard similarity measure.

def time_diff_milli(start, finish)
   (finish - start) * 1000.0
end

Recommendify.redis = Redis.new

class MyRecommender < Recommendify::Base

  # store only the top fifty neighbors per item
  max_neighbors 50

  # define an input data set "order_items". we'll add "order_id->product_id"
  # pairs to this input and use the jaccard coefficient to retrieve a 
  # "customers that ordered item i1 also ordered item i2" statement and apply
  # the result to the item<->item similarity matrix with a weight of 5.0
  input_matrix :order_items,  
    :native => true,
    :similarity_func => :jaccard,    
    :weight => 5.0

end

recommender = MyRecommender.new

# add `order_id->product_id` interactions to the order_item_sim input
# you can add data incrementally and call RecommendedItem.process! to update
# the similarity matrix at any time.
i = 0
input = File.new('rec2.out','r')
  input.each_line{
                |line| 
                #puts line
                i += 1
                if i % 1000 == 0
                  puts i
                end
                player_sc = line.split('-')
#                puts player_sc[1]
                player = player_sc[0]
#                puts player
                site_content = player_sc[1].split(',')
                site_content.pop()
#                puts site_content.length
                recommender.order_items.add_set(player,site_content)  
              }

# Calculate all elements of the similarity matrix
t1 = Time.now
recommender.process!
t2 = Time.now

puts time_diff_milli(t1,t2) 
# ...or calculate a specific row of the similarity matrix (a specific item)
# use this to avoid re-processing the whole matrix after incremental updates

# retrieve similar products to "product23"
#recommender.for("item23") 
#  => [ <Recommendify::Neighbor item_id:"product65" similarity:0.23>, (...) ]

# remove "product23" from the similarity matrix and the input matrices. you should 
# do this if your items 'expire', since it will speed up the calculation
#recommender.delete_item!("product23") 
