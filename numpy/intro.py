import numpy as np

num_list = [
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,15,16]]

np_list = np.array(num_list)

print(np_list[0:5:1]) #slice step cannot be zero.

#first two rows and first two columns

print(np_list[:2,:2])

#last two rows but the first two columns 

print(np_list[2:,2:])

#Exercise to calculate area

radii  = np.array([1,2,3,4])
area = np.pi * (radii ** 2)
print(np.round(area,2))

#comparison operators

scores = np.array([91,57,89,67,98,100])
print(scores >= 60)
scores[scores < 60] = 0
print(scores)

#broadcasting

array1 = np.array([[1,2,3,4,5,6,7,8,9,10]])
array2 = np.array([[1],[2],[3],[4],[5],[6],[7],[8],[9],[10]])

print(array1 * array2)

#aggregrate function

new_array = np.array([[1,2,3,4,5],[6,7,8,9,10]])

print(np.sum(new_array, axis=0))
print(np.sum(new_array, axis=1))
print(np.mean(new_array))
print(np.round(np.std(new_array), 2))
print(np.var(new_array))
print(np.argmin(new_array))
print(np.argmax(new_array))
print(np.min(new_array))
print(np.max(new_array))

#filter in numpy

students_age = np.array([[19,20,43,27,32,16],[23,29,31,25,27,17]])

teens = students_age[students_age <= 19]
adults = students_age[(students_age > 19) & (students_age < 65)]
seniors = students_age[students_age >= 65]
even = students_age[students_age % 2 == 0]
odd = students_age[students_age % 2 != 0]

print(teens, adults, seniors, even, odd)

#where function -- preserves shape of the function
# argument (condition, array, fill value) -- only fill those value who doesnt meet the condition
print(np.where(students_age <= 19, students_age, 0))

# random

rng = np.random.default_rng(seed =812)
randomness = np.array([["Apple"],["Banana"],["Coconut"]])
rng.shuffle(randomness)
print(randomness)
print(rng.choice(randomness, size=(2,3)))
print(rng.integers(low=1,high=7,size=6))

