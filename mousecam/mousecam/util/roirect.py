#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Arne F. Meyer <arne.f.meyer@gmail.com>
# License: GPLv3

"""
    Rectangular ROI selection
"""

from __future__ import print_function

import matplotlib.pyplot as plt

from ..io.video import get_first_frame


def selectROI(frame, verbose=False, title=None, bbox=None):

    from matplotlib.widgets import RectangleSelector
    from six import string_types

    if isinstance(frame, string_types):
        frame = get_first_frame(frame)

    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
    ax1.imshow(frame, vmin=0, vmax=255, cmap='gray')

    img2 = ax2.imshow(frame, vmin=0, vmax=255, cmap='gray')

    if title is not None:
        fig.suptitle(title)

    current_bbox = [0, 0, frame.shape[1], frame.shape[0]]

    # show given bbox if available
    rect = None
    if bbox is not None:

        from matplotlib.patches import Rectangle
        rect = Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3],
                         fc='r', alpha=.25)
        ax1.add_patch(rect)
        img2.set_data(frame[bbox[1]:bbox[1]+bbox[3],
                            bbox[0]:bbox[0]+bbox[2]])

        current_bbox = bbox

    def onselect(eclick, erelease):
        'eclick and erelease are matplotlib events at press and release'

        if verbose:
            print(' startposition : (%f, %f)' % (eclick.xdata, eclick.ydata))
            print(' endposition   : (%f, %f)' % (erelease.xdata,
                                                 erelease.ydata))
            print(' used button   : ', eclick.button)

        x1, y1 = int(eclick.xdata), int(eclick.ydata)
        x2, y2 = int(erelease.xdata), int(erelease.ydata)

        img2.set_data(frame[y1:y2, x1:x2])
        current_bbox[:] = [x1, y1, x2 - x1, y2-y1]

        if rect is not None and rect.axes is not None:
            rect.remove()

        if verbose:
            print("current bbox:", current_bbox)

    def toggle_selector(event):

        if event.key in [' ', 'enter']:
            # add selected region to list
            if len(current_bbox) > 0:
                if verbose:
                    print("added bbox:", current_bbox)
                plt.close()

    toggle_selector.RS = RectangleSelector(ax1, onselect, drawtype='box')
    plt.connect('key_press_event', toggle_selector)

    plt.show(block=True)

    return current_bbox
