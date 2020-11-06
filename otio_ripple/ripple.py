import opentimelineio as otio

EDIT_RATE = 24
HOUR = 3600 * EDIT_RATE
timeline = otio.adapters.read_from_file("sample_data/sample2.edl")
for clip in timeline.each_clip():
    ripple = -HOUR + 100

    start_frame = clip.source_range.start_time.value

    # SRC TC is less than an hour - don't ripple
    if start_frame < HOUR:
        ripple = 100

    end_frame = start_frame + clip.source_range.duration.value + ripple
    edl_meta = clip.metadata.get('cmx_3600',{})
    
    nucoda_stack = [
        'NUCODA_LAYER Log',
        'NUCODA_LAYER Log2',
        'NUCODA_LAYER Log3',
        'NUCODA_LAYER Log4',
        'NUCODA_LAYER Log5',
        'NUCODA_LAYER Log6',
    ]

    comments = edl_meta.get('comments', [])

    for comment in comments:
        if 'REEL:' in comment:
            _, reel_name = comment.split(": ")
            lut_layer = 'NUCODA_LAYER GT_LUT -effect NucodaCMSPath -lut T:\\luts\\GoodTrouble\\{}.cube'.format(reel_name)
            nucoda_stack.append(lut_layer)

    comments.extend(nucoda_stack)

    clip.source_range = otio.opentime.range_from_start_end_time(
        otio.opentime.from_frames(start_frame + ripple, EDIT_RATE),
        otio.opentime.from_frames(end_frame, EDIT_RATE)
    )

print(otio.adapters.write_to_string(timeline, adapter_name='cmx_3600'))
