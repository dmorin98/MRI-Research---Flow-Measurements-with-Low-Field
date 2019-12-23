ax1.errorbar(flowVelocity, BA_Data,
            xerr=OscErrorCCM,
            yerr=math.sqrt(residuals/len(BA_Data)),
            fmt='.k--', label='Actual Data')