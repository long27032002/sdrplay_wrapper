#!/usr/bin/env python3
import time
from tests.test_common import *

class SDRplayStreamingTest(SDRplayBaseTest):
    """Tests for streaming functionality common to all devices"""

    def setUp(self):
        super().setUp()  # Handle device creation/opening
        self.stream_data = None
        self.gain_data = None
        self.overload_data = None
        # We already have self.device_info from SDRplayBaseTest

    class StreamHandler(sdrplay.StreamCallbackHandler):
        def __init__(self, test_instance):
            # For abstract classes in SWIG, don't call the parent constructor
            self.test_instance = test_instance

        def handleStreamData(self, xi, xq, numSamples):
            import numpy as np
            self.test_instance.logger.debug(f"Stream data received: {numSamples} samples")
            
            # Verify that xi and xq are numpy arrays
            self.test_instance.assertTrue(isinstance(xi, np.ndarray), "xi is not a numpy array")
            self.test_instance.assertTrue(isinstance(xq, np.ndarray), "xq is not a numpy array")
            self.test_instance.assertEqual(xi.shape[0], numSamples, "xi array size mismatch")
            self.test_instance.assertEqual(xq.shape[0], numSamples, "xq array size mismatch")
            
            # Calculate the power to verify data is valid
            power = np.mean(xi.astype(np.float32)**2 + xq.astype(np.float32)**2)
            self.test_instance.logger.debug(f"Average power: {power:.2f}")
            
            self.test_instance.stream_data = (xi, xq, numSamples)

    class GainHandler(sdrplay.GainCallbackHandler):
        def __init__(self, test_instance):
            # For abstract classes in SWIG, don't call the parent constructor
            self.test_instance = test_instance

        def handleGainChange(self, gRdB, lnaGRdB, currGain):
            self.test_instance.logger.debug(
                f"Gain change: gRdB={gRdB}, lnaGRdB={lnaGRdB}, currGain={currGain}")
            self.test_instance.gain_data = (gRdB, lnaGRdB, currGain)

    class PowerHandler(sdrplay.PowerOverloadCallbackHandler):
        def __init__(self, test_instance):
            # For abstract classes in SWIG, don't call the parent constructor
            self.test_instance = test_instance

        def handlePowerOverload(self, isOverloaded):
            self.test_instance.logger.debug(f"Power overload: {isOverloaded}")
            self.test_instance.overload_data = isOverloaded

    def test_streaming_callbacks(self):
        """Test callback registration and basic streaming"""
        self.logger.info("Testing streaming callback registration and control")
        
        # Skip if no device available
        if not hasattr(self, 'device') or not self.device or not self.device_info:
            self.skipTest("No device available for testing")
            return
        
        # Check initial streaming state
        self.assertFalse(self.device.isStreaming())
        
        # Create and register callbacks (would be used in actual implementation)
        stream_cb = self.StreamHandler(self)
        gain_cb = self.GainHandler(self)
        power_cb = self.PowerHandler(self)
        
        # Register callbacks
        self.device.registerStreamCallback(stream_cb)
        self.device.registerGainCallback(gain_cb)
        self.device.registerPowerOverloadCallback(power_cb)
        
        # Start streaming
        result = self.device.startStreaming()
        self.assertTrue(result, "Failed to start streaming")
        self.assertTrue(self.device.isStreaming())
        
        # Let it run a short time
        self.logger.info("Streaming for 1 second...")
        time.sleep(1)
        
        # Stop streaming
        result = self.device.stopStreaming()
        self.assertTrue(result, "Failed to stop streaming")
        self.assertFalse(self.device.isStreaming())
        
        # Check that we received some callbacks
        self.assertIsNotNone(self.stream_data, "No stream data received")
        
        self.logger.info("Streaming control API works correctly")

if __name__ == '__main__':
    unittest.main(verbosity=2)
