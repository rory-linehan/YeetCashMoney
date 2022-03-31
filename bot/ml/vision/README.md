# vision

This package provides vision through machine learning techniques

## Images and annotations

You can use the scripts provided in `/Scripts` to generate images while
playing Runescape.
Currently the screenshots are in `.png` format.
I'm not sure if using another format will cause problems in the future,
so let's stick to `.png`.
*Make sure the filenames have no spaces or things could break!*

These need to be annotated using `labelImg`.
To install `labelImg`, execute the following command:

```bash
pip3 install labelImg
```

Open the directory where the screenshots are stored,
then create a separate corresponding directory for the annotations
using the `Change Save Dir` button in `labelImg`.
Draw boxes and label them, then save using the `PascalVOC` format.
You should see an XML file in the annotations directory that corresponds
with the screenshot.

Use the following naming convention for labels for consistency:

`screen_function_name`

The `name` part is optional,
since sometimes the function is the same as the name.
An example from the login screen:

`login_NewUser`
the name of the NewUser button is the same as the function,
and `login_button_NewUser` seems like a bit much for such a simple label.

For interacting with the bank in Runescape, use something like this:

`rs_bank_tab1`, `rs_bank_tab2`, etc.

When you add a label, if it is not in the `ml/vision/labels` file,
please add it there for it to automatically get picked up by the trainer.
