import tensorflow as tf
import time


class TrainModel():
    def __init__(self, model, image, targets, num_layers):
        super(TrainModel, self).__init__()
        # Set mendatory parameters
        self.model = model
        self.image = image
        self.style_targets = targets[0]
        self.content_targets = targets[1]
        self.num_style_layers = num_layers[0]
        self.num_content_layers = num_layers[1]

        # Set defaults for optional paramters
        self.epochs = 1
        self.steps_per_epoch = 100
        self.optimizer = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)
        # Regulates the importance of preserving content vs applying style
        self.content_weight = 1e-2
        self.style_weight = 1e4
        # Strength of the high pass filter
        self.total_variation_weight=30


    def set_optimizer(self, optimizer):
        self.optimizer = optimizer
    

    def set_epochs(self, epochs, steps_per_epoch):
        self.epochs = epochs
        self.steps_per_epoch = steps_per_epoch


    def set_content_style_ratio(self, content_weight, style_weight):
        self.content_weight = content_weight
        self.style_weight = style_weight


    def set_total_variation(self, total_variation_weight):
        self.total_variation_weight = total_variation_weight


    def get_time(self):
        """Returns the time it took to train"""
        return self.end_time - self.start_time


    def train(self):
        """Should return the transfered image"""
        self.start_time = time.time()

        step = 0
        for _ in range(self.epochs):
            for _ in range(self.steps_per_epoch):
                step += 1
                self._train_step()

        self.end_time = time.time()
        return self.image


    @tf.function()
    def _train_step(self):
        with tf.GradientTape() as tape:
            outputs = self.model(self.image)
            loss = self._style_content_loss(outputs)
            loss += self.total_variation_weight*tf.image.total_variation(self.image)

        grad = tape.gradient(loss, self.image)
        self.optimizer.apply_gradients([(grad, self.image)])
        self.image.assign(clip_0_1(self.image))

    
    def _style_content_loss(self, outputs):
        style_outputs = outputs['style']
        content_outputs = outputs['content']
        style_loss = type_loss(style_outputs, self.style_targets, self.style_weight, self.num_style_layers)
        content_loss = type_loss(content_outputs, self.content_targets, self.content_weight, self.num_content_layers)
        loss = style_loss + content_loss
        return loss


def mse(base_content, target):
    return tf.reduce_mean(tf.square(base_content - target))


def clip_0_1(image):
  return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)


# Bin hier mit dem Namen noch nicht zufrieden, gerne Vorschläge machen
def type_loss(output, target, weight, num_layers):
    type_loss = tf.add_n([mse(output[name], target[name]) for name in output.keys()])
    type_loss *= weight / num_layers
    return type_loss

    
