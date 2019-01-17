# just create some sample data
space <- sample(seq_len(100), 60)


index <- sample(seq_along(space), 1)
steps <- index
current_value <- space[index]

neighbor <- ifelse(space[index+1] > space[index-1],
                   space[index+1], space[index+1])

index <- ifelse(space[index+1] == neighbor,
                index+1, index-1)

# climb that hill
while (current_value <= neighbor) {
  # neighbor <- ifelse(current > space[index-1], 
  #                    space[index+1], space[index-1])
  neighbor <- ifelse(space[index+1] > space[index-1],
                     space[index+1], space[index+1])
  
  index <- ifelse(space[index+1] == neighbor,
                  index+1, index-1)
  
  if (neighbor <= current_value) {
    steps <- c(steps, index)
    return(current_value)
  } else {
    steps <- c(steps, index)
    current_value <- neighbor
  }
}
