#pragma once
#include "device_types.h"
#include "sdrplay_api.h"
#include <memory>
#include <vector>
#include <functional>

namespace sdrplay {

// Forward declarations for callback handlers
class StreamCallbackHandler;
class GainCallbackHandler;
class PowerOverloadCallbackHandler;

class DeviceControl {
public:
    DeviceControl();
    virtual ~DeviceControl();

    // Device management
    virtual bool open();
    virtual void close();
    virtual float getApiVersion() const;
    virtual std::vector<DeviceInfo> getAvailableDevices();
    virtual bool selectDevice(const DeviceInfo& deviceInfo);
    virtual bool releaseDevice();

    // Device access
    virtual sdrplay_api_DeviceT* getCurrentDevice() const;
    virtual sdrplay_api_DeviceParamsT* getDeviceParams() const;
    virtual std::string getLastError() const;

    // Common control methods
    virtual void setFrequency(double freq) = 0;
    virtual double getFrequency() const = 0;
    virtual void setSampleRate(double rate) = 0;
    virtual double getSampleRate() const = 0;

    // RSP1A specific controls
    virtual void setGainReduction(int gain) = 0;
    virtual void setLNAState(int state) = 0;

    // RSPdxR2 specific controls
    virtual void setHDRMode(bool enable) = 0;
    virtual void setBiasTEnabled(bool enable) = 0;
    
    // Streaming control methods
    virtual bool initializeStreaming() = 0;
    virtual bool startStreaming() = 0;
    virtual bool stopStreaming() = 0;
    virtual bool isStreaming() const = 0;
    
    // Callback registration
    virtual void setStreamCallback(StreamCallbackHandler* handler) = 0;
    virtual void setGainCallback(GainCallbackHandler* handler) = 0;
    virtual void setPowerOverloadCallback(PowerOverloadCallbackHandler* handler) = 0;

protected:
    struct Impl;
    std::unique_ptr<Impl> impl;
};

} // namespace sdrplay
