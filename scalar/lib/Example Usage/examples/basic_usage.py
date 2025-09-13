#!/usr/bin/env python3
"""
Basic usage example for SAN Automation Library
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from san_automation import (
    ConfigManager,
    SanAutomationOrchestrator,
    get_vendor_class,
    get_host_class,
    setup_logging
)

def main():
    # Setup logging
    setup_logging()
    
    # Load configuration
    config_manager = ConfigManager("config.json")
    config = config_manager.load_config()
    
    # Get appropriate vendor and host classes
    VendorClass = get_vendor_class(config.vendor_type)
    HostClass = get_host_class(config.host_type)
    
    # Create manager instances
    san_manager = VendorClass(config)
    host_manager = HostClass(config)
    
    # Create orchestrator
    orchestrator = SanAutomationOrchestrator(san_manager, host_manager)
    
    try:
        # Run full automation
        if orchestrator.initialize_connections():
            if orchestrator.create_storage_infrastructure():
                if orchestrator.configure_host_storage():
                    orchestrator.run_performance_test()
        
        # Print status report
        status = orchestrator.get_status_report()
        print("Automation completed!")
        print(f"Success: {status['success']}")
        
    finally:
        orchestrator.cleanup()

if __name__ == "__main__":
    main()
