# Magnification Calculation Program
[Video Guide]
## Description
The `cal_mag` module takes in a dataset of interest (most likely a capture of
the  USAFT) as an argument and previews the full FOV image. On the `matplotlib`
preview the user is then able to hover over the upper-left and lower-right
coordinates (to make a square/rectangle) of the region of interest (ROI), and
enter them as parameters through the CLI. Subsequently, the preview will be
updated with the ROI, and the user would then be able to enter in parameters for
the vertical bar (vbar) placed on the target bars.

## `metadata.json`
For this module and to organize and characterize datasets, a metadata file is
created in the `datasets` directory if not pre-existing.

The dictionary is structured as follows:

```
{
    <dataset_filename>: {
        "roi": {
            "x0": ,
            "y0": ,
            "x1": ,
            "y1": ,
        },
        "vbar": {
            "x" : ,
            "y0": ,
            "y1": ,
        }
    },
}
```

Each dataset entry is organized by its unique pathname. The dataset parameters
can be updated if needed. This will hopefully add a software layer of
characterization for each dataset so the user does not have to manually keep
track of parameters for subsequent experiments.

[Video Guide]: https://youtu.be/5KWWd2UEgpk?si=eYq85EYGG-zUdj5x
