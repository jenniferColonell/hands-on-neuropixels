# -*- coding: utf-8 -*-

import time
from sglx_pkg import sglx

# Edit the server address/port here
sglx_addr = "localhost"
sglx_port = 4142


# Plays wave variable wavenme at OneBox channel AO-0.
# playback is triggered by a hardware signal at 
#
def wp_soft_start():

    # Handle to SpikeGLX
    hSglx = sglx.c_sglx_createHandle()
    ok    = sglx.c_sglx_connect( hSglx, sglx_addr.encode(), sglx_port )

    if ok:
        # For demo purposes we assume the OneBox is not recording...
        # So we refer to it using its slot index
        ip = -1
        slot = 20

        # Load the wave plan
        wave_name = '5V_sq_multi'
        # time for the wave to play, in seconds. Get a value by hitting 'Check'
        # in the Wave Planner dialog.
        wave_time = 6  
        n_iter = 2  # number of times to play the whole wave

        ok = sglx.c_sglx_obx_wave_load( hSglx, ip, slot, wave_name.encode() )

        if ok:
            # Select AI-3 triggering and no looping, no loop
            trigger = 3
            looping = False
            ok = sglx.c_sglx_obx_wave_arm( hSglx, ip, slot, trigger, looping )

            if ok:
                # Start playback now, output is always at AO-0
                
                for i in range(n_iter):
                    # write 5V to channel 1. Connect AIO1 to AIO3 on breakout board.
                    ch_volt = f'(1,5.0)'
                    ok = sglx.c_sglx_obx_AO_set(hSglx, ip, slot, ch_volt.encode() )
                    if ok:                   
                        print(f'iteration: {i}')
                        time.sleep(0.05)
                        ch_volt = f'(1,0.0)'
                        ok = sglx.c_sglx_obx_AO_set(hSglx, ip, slot, ch_volt.encode() )
                        time.sleep(wave_time + 0.1)
                    else:
                        break #come out of loop     
                ok = sglx.c_sglx_obx_wave_startstop( hSglx, ip, slot, False )

    if not ok:
        print( "error [{}]\n".format( sglx.c_sglx_getError( hSglx ) ) )

    sglx.c_sglx_close( hSglx )
    sglx.c_sglx_destroyHandle( hSglx )


if __name__ == "__main__":
    wp_soft_start()


