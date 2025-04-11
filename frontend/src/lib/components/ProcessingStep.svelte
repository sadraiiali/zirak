<script>
    import { createEventDispatcher } from "svelte";
    import {
        CheckCircle,
        Loader2,
        CircleDashed,
        ChevronDown,
        XCircle, // Icon for error status
    } from "@lucide/svelte";

    let {
        status = "pending", // Default status
        title = "Untitled Step",
        timeTook = undefined,
        parameters = undefined,
        isExpanded = false, // Default to collapsed
    } = $props();

    // --- State Caching & Animation Logic ---
    // Cache previous status locally within the component's state
    let prevStatus = $state(status);
    let highlightClass = $state(""); // Temporary class for highlight animations
    let animationTimeoutId = $state(null);
    // --- End State Caching & Animation Logic ---

    const dispatch = createEventDispatcher();

    function handleToggleExpand() {
        dispatch("toggleExpand");
    }

    // Reactive state for dynamic class and icon component
    let containerClass = $derived("");
    let statusIconComponent = $derived(null);

    $effect(() => {
        // Clear any pending animation timeout from previous renders/changes
        clearTimeout(animationTimeoutId);

        // --- Handle Status Change Animation ---
        // Compare current status prop with the cached previous status
        if (status !== prevStatus) {
            // Apply specific animation class based on the state transition
            if (prevStatus === "pending" && status === "processing") {
                highlightClass = "highlight-processing";
                // Automatically remove the class after the animation completes
                animationTimeoutId = setTimeout(() => {
                    highlightClass = "";
                }, 1200); // Duration matches CSS animation
            } else if (status === "complete" || status === "error") {
                // Apply a different subtle animation for completion/error
                highlightClass = "highlight-finish";
                animationTimeoutId = setTimeout(() => {
                    highlightClass = "";
                }, 600); // Duration matches CSS transition/effect
            } else {
                highlightClass = ""; // Ensure class is removed if no specific animation needed
            }
            // Update the cached previous status *after* comparison for the next change
            prevStatus = status;
        }
        // --- End Status Change Animation ---

        // Determine base class and icon based on *current* status
        let baseClass = "processing-step";
        switch (status) {
            case "complete":
                containerClass = `${baseClass} status-complete`;
                statusIconComponent = CheckCircle;
                break;
            case "processing":
                containerClass = `${baseClass} status-processing`;
                statusIconComponent = Loader2;
                break;
            case "error":
                containerClass = `${baseClass} status-error`;
                statusIconComponent = XCircle;
                break;
            case "pending":
            default:
                containerClass = `${baseClass} status-pending`;
                statusIconComponent = CircleDashed;
                break;
        }
    });

    // Chevron rotation class
    let chevronClass = $derived(isExpanded ? "chevron-rotated" : "");

    // Details container max-height for transition
    let detailsStyle = $derived(
        isExpanded ? "max-height: 1000px;" : "max-height: 0;",
    ); // Adjust max-height if needed

    // Check if parameters object has own enumerable properties
    let hasParameters = $derived(
        parameters && Object.keys(parameters).length > 0,
    );
</script>

<div class="{containerClass} {highlightClass}">
    <div class="step-header">
        <div class="step-icon-wrapper">
            {#if statusIconComponent}
                <svelte:component
                    this={statusIconComponent}
                    class="step-icon status-icon-{status}"
                    size={16}
                />
            {/if}
        </div>
        <div class="step-title-wrapper">
            <p class="step-title">{title}</p>
        </div>
        <div class="step-tools">
            <slot name="tools"></slot>
        </div>
        <div class="step-meta-toggle">
            {#if status === "complete" && timeTook != null}
                <span class="step-meta-text">({timeTook})</span>
            {/if}
            {#if status === "processing"}
                <span class="step-meta-text text-processing">Running...</span>
            {/if}
            {#if status === "error"}
                <span class="step-meta-text text-error">Error</span>
            {/if}
            <button
                class="btn btn-ghost btn-icon-xs btn-toggle-expand"
                title={isExpanded ? "Collapse Details" : "Expand Details"}
                onclick={handleToggleExpand}
                aria-expanded={isExpanded}
            >
                <ChevronDown size="16" class="chevron-icon {chevronClass}" />
            </button>
        </div>
    </div>

    <div
        class="step-details-container"
        style={detailsStyle}
        aria-hidden={!isExpanded}
    >
        <div class="step-details-content">
            {#if hasParameters}
                <div class="step-parameters">
                    <h4 class="parameters-title">Parameters</h4>
                    <dl class="parameters-list">
                        {#each Object.entries(parameters) as [key, value]}
                            <div class="parameter-item">
                                <dt class="parameter-key">{key}</dt>
                                <dd class="parameter-value">
                                    {JSON.stringify(value)}
                                </dd>
                            </div>
                        {/each}
                    </dl>
                </div>
            {/if}

            <div class="step-body">
                <slot name="body"></slot>
            </div>
        </div>
    </div>
</div>

<style>
    /* Ensure :root CSS Variables are defined globally or imported */
    :root {
        --background: 0 0% 100%;
        --foreground: 222.2 84% 4.9%;
        --muted: 210 40% 96.1%;
        --muted-foreground: 215.4 16.3% 46.9%;
        --card: 0 0% 100%;
        --card-foreground: 222.2 84% 4.9%;
        --border: 214.3 31.8% 91.4%;
        --primary: 221.2 83.2% 53.3%;
        --secondary: 210 40% 96.1%;
        --secondary-foreground: 222.2 47.4% 11.2%;
        --accent: 210 40% 96.1%;
        --accent-foreground: 222.2 47.4% 11.2%;
        --destructive: 0 84.2% 60.2%;
        --ring: 221.2 83.2% 53.3%;
        --radius: 0.5rem;
        --teal-500: 163 70% 45%;
        --teal-600: 163 75% 40%;
        --blue-100: 212 100% 94%;
        --blue-500: 217 91% 60%;
        --blue-600: 217 91% 55%;
        --red-500: 0 72% 51%;
        --muted-alpha-30: hsla(var(--muted), 0.3);
        /* Colors for animations */
        --processing-glow: hsla(var(--blue-500), 0.3);
        --finish-glow: hsla(var(--teal-500), 0.2);
    }

    .processing-step {
        border: 1px solid hsl(var(--border));
        background-color: hsl(var(--card));
        border-radius: var(--radius);
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        overflow: hidden; /* Important for border-radius and potential pseudo-elements */
        border-left-width: 4px;
        /* Transitions for properties that change smoothly between states */
        transition:
            opacity 0.2s ease-in-out,
            border-color 0.3s ease-in-out,
            box-shadow 0.3s ease-in-out;
        margin-bottom: 0.5rem;
        position: relative; /* Context for potential absolute positioned elements or pseudo-elements */
    }

    /* --- Status Specific Styles --- */
    .status-pending {
        border-left-color: hsl(var(--border));
        opacity: 0.8;
    }
    .status-pending:hover {
        opacity: 1;
    }
    .status-processing {
        border-left-color: hsl(var(--blue-500));
    }
    .status-complete {
        border-left-color: hsl(var(--teal-500));
    }
    .status-error {
        border-left-color: hsl(var(--destructive));
    }

    /* --- Highlight Animations --- */
    /* Keyframes for the pulse effect when starting processing */
    @keyframes pulse-glow-processing {
        0% {
            box-shadow:
                0 1px 2px 0 rgba(0, 0, 0, 0.05),
                0 0 0 0px var(--processing-glow);
        }
        50% {
            box-shadow:
                0 2px 4px 0 rgba(0, 0, 0, 0.07),
                0 0 0 5px var(--processing-glow);
        } /* Highlight shadow */
        100% {
            box-shadow:
                0 1px 2px 0 rgba(0, 0, 0, 0.05),
                0 0 0 0px var(--processing-glow);
        } /* Return to normal shadow */
    }

    /* Class applied temporarily during the pending -> processing transition */
    .highlight-processing {
        animation: pulse-glow-processing 1.2s ease-out forwards;
    }

    /* Class applied temporarily during finish transition */
    .highlight-finish {
        /* Example: Flash the border color more intensely */
        border-color: hsl(
            var(--teal-600)
        ); /* Make border color briefly stronger */
        /* The standard transition on .processing-step handles the fade back */
    }
    /* Ensure the standard transition applies when highlight is not active */
    .processing-step:not(.highlight-finish):not(.highlight-processing) {
        transition:
            opacity 0.2s ease-in-out,
            border-color 0.3s ease-in-out,
            box-shadow 0.3s ease-in-out;
    }

    /* --- Step Header --- */
    .step-header {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        gap: 0.75rem;
        position: relative;
        z-index: 1; /* Ensure header content is above animated background/shadows */
    }
    .step-icon-wrapper {
        flex-shrink: 0;
        line-height: 1;
    }
    .step-icon {
        display: block;
    }
    .status-icon-complete {
        color: hsl(var(--teal-600));
    }
    .status-icon-processing {
        color: hsl(var(--blue-600));
        animation: spin 1s linear infinite;
    }
    .status-icon-pending {
        color: hsl(var(--muted-foreground));
    }
    .status-icon-error {
        color: hsl(var(--destructive));
    }
    .step-title-wrapper {
        flex-grow: 1;
        min-width: 0;
    }
    .step-title {
        font-weight: 500;
        font-size: 0.875rem;
        color: hsl(var(--card-foreground));
        margin: 0;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .step-tools {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        flex-shrink: 0;
    }
    .step-meta-toggle {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        flex-shrink: 0;
        margin-left: auto;
    }
    .step-meta-text {
        font-size: 0.75rem;
        color: hsl(var(--muted-foreground));
        white-space: nowrap;
    }
    .text-processing {
        color: hsl(var(--blue-600));
    }
    .text-error {
        color: hsl(var(--destructive));
        font-weight: 500;
    }
    .btn-toggle-expand {
        color: hsl(var(--muted-foreground));
    }
    .chevron-icon {
        transition: transform 0.2s ease-in-out;
        display: block;
    }
    .chevron-rotated {
        transform: rotate(180deg);
    }

    /* --- Step Details (Collapsible Area) --- */
    .step-details-container {
        border-top: 1px solid hsl(var(--border));
        background-color: var(--muted-alpha-30); /* Subtle background */
        overflow: hidden;
        /* Transitions for smooth expand/collapse */
        transition:
            max-height 0.3s ease-out,
            opacity 0.3s ease-out,
            visibility 0.3s;
        opacity: 1;
        visibility: visible;
    }
    .step-details-container[aria-hidden="true"] {
        max-height: 0 !important; /* Use !important cautiously, but useful here */
        opacity: 0;
        visibility: hidden;
        transition:
            max-height 0.2s ease-in,
            opacity 0.15s ease-in,
            visibility 0s linear 0.2s;
        border-top-color: transparent; /* Hide border when fully collapsed */
    }
    .step-details-content {
        padding: 0.75rem; /* Base padding */
        padding-left: calc(
            0.75rem + 16px + 0.75rem
        ); /* Align content with title (padding + icon + gap) */
        display: flex;
        flex-direction: column;
        gap: 0.75rem; /* Space between Parameters and Body Slot */
    }

    /* --- Parameters Section (Improved Table Styling) --- */
    .step-parameters {
        padding-top: 0.25rem; /* Small space above */
    }
    .parameters-title {
        font-size: 0.75rem;
        font-weight: 600;
        color: hsl(var(--muted-foreground));
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin: 0 0 0.5rem 0;
        padding-bottom: 0.25rem;
        border-bottom: 1px solid hsl(var(--border)); /* Separator line under title */
    }
    .parameters-list {
        font-size: 0.8rem; /* Slightly larger than text-xs for readability */
        margin: 0;
        padding: 0;
        list-style: none; /* Remove default dl styling */
    }
    .parameter-item {
        display: grid;
        /* Grid layout: Key takes needed space, Value takes the rest */
        grid-template-columns: max-content 1fr;
        gap: 0.75rem; /* Gap between key and value */
        padding: 0.3rem 0; /* Vertical padding for spacing */
        align-items: baseline; /* Align text baselines nicely */
        /* Subtle separator between items */
        border-bottom: 1px solid hsla(var(--border), 0.4);
    }
    .parameter-item:last-child {
        border-bottom: none; /* Remove border from last item */
    }
    .parameter-key {
        font-weight: 500;
        color: hsl(var(--secondary-foreground)); /* Darker key text */
        text-align: right; /* Align key text to the right */
        white-space: nowrap; /* Prevent key from wrapping */
    }
    /* Add colon visually without adding it to the data */
    .parameter-key::after {
        content: ":";
    }
    .parameter-value {
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo,
            Courier, monospace; /* Monospace font */
        color: hsl(var(--foreground)); /* Standard text color for value */
        word-break: break-all; /* Allow long values to wrap */
        text-align: left;
        /* Subtle background for value distinction */
        background-color: hsla(var(--muted), 0.2);
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        line-height: 1.3;
    }

    /* --- Body Slot --- */
    /* Add some minimal top margin if parameters are also present */
    .step-parameters + .step-body {
        margin-top: 0.25rem;
    }
    /* Default styling for paragraphs within the body slot */
    .step-body :global(p) {
        font-size: 0.875rem;
        color: hsl(var(--muted-foreground)); /* Standard muted text color */
        line-height: 1.4;
        margin: 0;
    }
    .step-body :global(p:not(:first-child)) {
        margin-top: 0.5rem; /* Space between paragraphs */
    }

    /* --- Reusable Button Styles (Minimal set) --- */
    .btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        white-space: nowrap;
        border-radius: calc(var(--radius) - 2px);
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.15s ease-in-out;
        cursor: pointer;
        user-select: none;
        border: 1px solid transparent;
        background-color: transparent;
    }
    .btn:focus-visible {
        outline: 2px solid transparent;
        outline-offset: 2px;
        box-shadow:
            0 0 0 2px hsl(var(--background)),
            0 0 0 4px hsl(var(--ring));
    }
    .btn:disabled {
        pointer-events: none;
        opacity: 0.5;
    }
    .btn-icon-xs {
        height: 2rem;
        width: 2rem;
        padding: 0;
    }
    .btn-ghost {
        color: hsl(var(--secondary-foreground));
    }
    .btn-ghost:hover {
        background-color: hsl(var(--accent));
        color: hsl(var(--accent-foreground));
    }
    .btn-ghost.btn-toggle-expand {
        color: hsl(var(--muted-foreground));
    }
    .btn-outline {
        border-color: hsl(var(--border));
        background-color: hsl(var(--background));
        color: hsl(var(--secondary-foreground));
    }
    .btn-outline:hover {
        background-color: hsl(var(--accent));
        color: hsl(var(--accent-foreground));
    }
    .btn-xs {
        height: 2rem;
        padding-left: 0.625rem;
        padding-right: 0.625rem;
        font-size: 0.75rem;
    }
    .btn-xs > svg {
        width: 0.75rem;
        height: 0.75rem;
        margin-right: 0.25rem;
    }

    /* --- Animation Keyframes --- */
    @keyframes spin {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
</style>
