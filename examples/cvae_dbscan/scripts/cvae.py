import os
import click
from keras.optimizers import RMSprop
from molecules.utils import open_h5
from molecules.ml.unsupervised import (VAE, EncoderConvolution2D, 
                                       DecoderConvolution2D)
from molecules.ml.unsupervised.callback import (EmbeddingCallback,
                                                LossHistory) 


def validate_path(ctx, param, value):
    """
    Adds abspath to non-None file
    """
    if value:
        path = os.path.abspath(value)
        if not os.path.exists(path):
            raise click.BadParameter(f'path does not exist {path}')
        return path

# TODO: take epoch, batch_size, etc as arguments

@click.command()
@click.option('-i', '--input', 'input_path', default='cvae_input.h5',
              callback=validate_path,
              help='Input: OpenMM simulation path')
@click.option('-o', '--out', 'out_path', required=True,
              callback=validate_path,
              help='Output directory for model data')
@click.option('-d', '--latet_dim', default=3, type=int,
             help='Number of dimensions in latent space')
@click.option('-g', '--gpu', default=0, type=int,
             help='GPU id')
def main(input_path, out_path, latet_dim, gpu):

    # Set CUDA environment variables
    os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
    os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)

    with open_h5(input_path) as input_file:

        # Access contact matrix data from h5 file
        data = input_file['contact_maps']

        # Train validation split index
        split = int(0.8 * len(data))

        # Partition input data into 80-20 train valid split
        train, valid = data[:split], data[split:]

        input_shape = train.shape

        encoder = EncoderConvolution2D(input_shape=input_shape)

        # Get shape attributes of the last encoder layer to define the decoder
        encode_conv_shape, num_conv_params = encoder.get_final_conv_params()

        decoder = DecoderConvolution2D(output_shape=input_shape,
                                       enc_conv_params=num_conv_params,
                                       enc_conv_shape=encode_conv_shape)

        optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)

        cvae = VAE(input_shape=input_shape,
                   encoder=encoder,
                   decoder=decoder,
                   optimizer=optimizer)

        # Define callbacks to report model performance for analysis
        embed_callback = EmbeddingCallback(train, cvae)
        loss_callback = LossHistory()

        cvae.train(data=train, validation_data=valid, 
                   batch_size=512, epochs=100, 
                   callbacks=[embed_callback, loss_callback])

        # Define file paths to store model performance and weights 
        weight_path = os.path.join(out_path, 'weight.h5')
        embed_path = os.path.join(out_path, 'embed.npy')
        idx_path = os.path.join(out_path, 'embed-idx.npy')
        loss_path = os.path.join(out_path, 'loss.npy')
        val_loss_path = os.path.join(out_path, 'val-loss.npy')

        # Save model performance and weights
        cvae.save_weights(weight_path)
        embed_callback.save(embed_path=embed_path, idx_path=idx_path)
        loss_callback.save(loss_path=loss_path, val_loss_path=val_loss_path)


if __name__ == '__main__':
    main()
