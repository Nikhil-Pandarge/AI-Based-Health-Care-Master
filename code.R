#--------------------------

# Disease predction with Symptoms analysis

# @author Nikhil N Pandarge

# @author Pradip S Bhusnar

#--------------------------


getwd()

bc_data <- read.table("breast-cancer-wisconsin.data", 
                      header = FALSE, 
                      sep = ",")
head(bc_data)

colnames(bc_data) <- c("sample_code_number", 
                       "clump_thickness", 
                       "uniformity_of_cell_size", 
                       "uniformity_of_cell_shape", 
                       "marginal_adhesion", 
                       "single_epithelial_cell_size", 
                       "bare_nuclei", 
                       "bland_chromatin", 
                       "normal_nucleoli", 
                       "mitosis", 
                       "classes")

head(bc_data)

bc_data$classes <- ifelse(bc_data$classes == "2", "benign",
                          ifelse(bc_data$classes == "4", "malignant", NA))

bc_data[bc_data == "?"] <- NA

#how many NAs are in the data

length(which(is.na(bc_data)))

# how many samples would we loose, if we removed them?

nrow(bc_data)

nrow(bc_data[is.na(bc_data), ])

#--------------------------
# impute missing data

library(mice)

install.packages("mice")

bc_data[,2:10] <- apply(bc_data[, 2:10], 2, function(x) as.numeric(as.character(x)))
dataset_impute <- mice(bc_data[, 2:10],  print = FALSE)
bc_data <- cbind(bc_data[, 11, drop = FALSE], mice::complete(dataset_impute, 1))

bc_data$classes <- as.factor(bc_data$classes)

# how many benign and malignant cases are there?

summary(bc_data$classes)

library(ggplot2)

ggplot(bc_data, aes(x = classes, fill = classes)) +
  geom_bar()

ggplot(bc_data, aes(x = clump_thickness)) +
  geom_histogram(bins = 10)
#--------------------------
# principal component analysis:

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager")

BiocManager::install("pcaGoPromoter")

library(pcaGoPromoter)

library(ellipse)

# perform pca and extract scores

pcaOutput <- pca(t(bc_data[, -1]), printDropped = FALSE, scale = TRUE, center = TRUE)
pcaOutput2 <- as.data.frame(pcaOutput$scores)

# define groups for plotting

pcaOutput2$groups <- bc_data$classes

centroids <- aggregate(cbind(PC1, PC2) ~ groups, pcaOutput2, mean)

conf.rgn  <- do.call(rbind, lapply(unique(pcaOutput2$groups), function(t)
  data.frame(groups = as.character(t),
             ellipse(cov(pcaOutput2[pcaOutput2$groups == t, 1:2]),
                     centre = as.matrix(centroids[centroids$groups == t, 2:3]),
                     level = 0.95),
             stringsAsFactors = FALSE)))

ggplot(data = pcaOutput2, aes(x = PC1, y = PC2, group = groups, color = groups)) + 
  geom_polygon(data = conf.rgn, aes(fill = groups), alpha = 0.2) +
  geom_point(size = 2, alpha = 0.6) + 
  scale_color_brewer(palette = "Set1") +
  labs(color = "",
       fill = "",
       x = paste0("PC1: ", round(pcaOutput$pov[1], digits = 2) * 100, "% variance"),
       y = paste0("PC2: ", round(pcaOutput$pov[2], digits = 2) * 100, "% variance")) 

#--------------------------
library(tidyr)

gather(bc_data, x, y, clump_thickness:mitosis) %>%
  ggplot(aes(x = y, color = classes, fill = classes)) +
  geom_density(alpha = 0.3) +
  facet_wrap( ~ x, scales = "free", ncol = 3)

#--------------------------
# configure multicore
install.packages("doParallel")


library(doParallel)

cl <- makeCluster(detectCores())
registerDoParallel(cl)

library(caret)

#Training, validation and test data

set.seed(42)
index <- createDataPartition(bc_data$classes, p = 0.7, list = FALSE)
train_data <- bc_data[index, ]
test_data  <- bc_data[-index, ]

library(dplyr)

rbind(data.frame(group = "train", train_data),
      data.frame(group = "test", test_data)) %>%
  gather(x, y, clump_thickness:mitosis) %>%
  ggplot(aes(x = y, color = group, fill = group)) +
  geom_density(alpha = 0.3) +
  facet_wrap( ~ x, scales = "free", ncol = 3)

set.seed(42)
model_glm <- caret::train(clump_thickness ~ .,
                          data = train_data,
                          method = "glm",
                          preProcess = c("scale", "center"),
                          trControl = trainControl(method = "repeatedcv", 
                                                   number = 10, 
                                                   repeats = 10, 
                                                   savePredictions = TRUE, 
                                                   verboseIter = FALSE))
model_glm


predictions <- predict(model_glm, test_data)

# model_glm$finalModel$linear.predictors == model_glm$finalModel$fitted.values
 
# residual is difference between observed value and predicted value.

data.frame(residuals = resid(model_glm),
           predictors = model_glm$finalModel$linear.predictors) %>%
  ggplot(aes(x = predictors, y = residuals)) +
  geom_jitter() +
  geom_smooth(method = "lm")

# y == train_data$clump_thickness:

data.frame(residuals = resid(model_glm),
           y = model_glm$finalModel$y) %>%
  ggplot(aes(x = y, y = residuals)) +
  geom_jitter() +
  geom_smooth(method = "lm")
#--------------------------
#Classification:

library(rpart)

library(rpart.plot)

set.seed(42)

fit <- rpart(classes ~ .,
             data = train_data,
             method = "class",
             control = rpart.control(xval = 10, 
                                     minbucket = 2, 
                                     cp = 0), 
             parms = list(split = "information"))

rpart.plot(fit, extra = 100)
#--------------------------
#rain forest

set.seed(42)
model_rf <- caret::train(classes ~ .,
                         data = train_data,
                         method = "rf",
                         preProcess = c("scale", "center"),
                         trControl = trainControl(method = "repeatedcv", 
                                                  number = 10, 
                                                  repeats = 10, 
                                                  savePredictions = TRUE, 
                                                  verboseIter = FALSE))


model_rf$finalModel$confusion


imp <- model_rf$finalModel$importance
imp[order(imp, decreasing = TRUE), ]


# estimate variable importance

importance <- varImp(model_rf, scale = TRUE)
plot(importance)

confusionMatrix(predict(model_rf, test_data), test_data$classes)

results <- data.frame(actual = test_data$classes,
                      predict(model_rf, test_data, type = "prob"))

results$prediction <- ifelse(results$benign > 0.5, "benign",
                             ifelse(results$malignant > 0.5, "malignant", NA))

results$correct <- ifelse(results$actual == results$prediction, TRUE, FALSE)

ggplot(results, aes(x = prediction, fill = correct)) +
  geom_bar(position = "dodge")

ggplot(results, aes(x = prediction, y = benign, color = correct, shape = correct)) +
  geom_jitter(size = 3, alpha = 0.6)

#--------------------------
#Feature Selection:

library(corrplot)

# calculate correlation matrix
corMatMy <- cor(train_data[, -1])
corrplot(corMatMy, order = "hclust")
