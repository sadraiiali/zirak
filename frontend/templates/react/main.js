const { useState, useEffect, useRef, Fragment } = React; // Destructure React features

// --- Reusable Components ---

// Icon Component (Helper) - Updated default size
function Icon({ name, className = "w-3.5 h-3.5" }) { // UPDATED Default size
    const iconRef = useRef(null);

    useEffect(() => {
        let isMounted = true;
        if (iconRef.current && name) {
            const key = `${name}-${className}-${Date.now()}`;
             iconRef.current.innerHTML = '';
             iconRef.current.setAttribute('data-lucide-key', key);

            lucide.createIcons({
                nodes: [iconRef.current],
                attrs: {
                    'class': className,
                    'data-lucide': name
                 },
                name
            });

        } else if (iconRef.current && !name) {
            iconRef.current.innerHTML = '';
        }

        return () => { isMounted = false; };
    }, [name, className]);

    return <span ref={iconRef} data-lucide={name} key={`${name}-${className}`}></span>;
}


// Sidebar Component - Uses smaller default icons
function Sidebar() {
    useEffect(() => {
        const sidebarElement = document.querySelector('aside');
        if (sidebarElement) {
            lucide.createIcons({ context: sidebarElement });
        }
    }, []);

    return (
        <aside className="hidden md:flex md:flex-shrink-0">
            <div className="flex w-16 flex-col items-center border-r border-border bg-background py-4">
                <div className="flex flex-shrink-0 items-center justify-center h-10 w-10 mb-6" data-tooltip="Mastodon AI Design System">
                    <Icon name="palette" className="h-5 w-5 text-primary" /> {/* Keep logo slightly larger */}
                </div>
                <nav className="flex flex-col items-center flex-1 space-y-2 mt-2">
                    {/* Icons now use default w-3.5 h-3.5 */}
                    <a href="#overview" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" aria-current="page" data-tooltip="Overview">
                        <Icon name="book-open" />
                    </a>
                    <a href="#foundations" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="Foundations">
                        <Icon name="layers" />
                    </a>
                    <a href="#layout" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="Layout">
                        <Icon name="layout-template" />
                    </a>
                    <a href="#components" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="Components">
                        <Icon name="puzzle" />
                    </a>
                    <a href="#components-buttons" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="Buttons">
                       <Icon name="mouse-pointer-click" />
                    </a>
                     <a href="#components-avatar" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="Avatar">
                       <Icon name="circle-user-round" />
                    </a>
                     <a href="#components-userinfo" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="User Info Block">
                       <Icon name="contact" />
                    </a>
                     <a href="#components-blockquote" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="Blockquote">
                       <Icon name="quote" />
                    </a>
                     <a href="#components-checkbox" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="Checkbox Switch">
                       <Icon name="toggle-right" />
                    </a>
                    <a href="#components-messagebox" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="Message Box">
                       <Icon name="message-square" />
                    </a>
                     <a href="#components-modal" className="nav-link relative text-muted-foreground hover:bg-accent hover:text-accent-foreground flex items-center justify-center rounded-md h-10 w-10 text-sm font-medium" data-tooltip="Modal">
                       <Icon name="copy" />
                    </a>
                    {/* ... other component links */}
                </nav>
                <div className="mt-auto flex flex-shrink-0 items-center justify-center pt-4">
                    <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="relative group block" data-tooltip="View on GitHub">
                        <Icon name="github" className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" /> {/* Smaller GitHub icon */}
                    </a>
                </div>
            </div>
        </aside>
    );
}

// Header Component
function Header() {
    useEffect(() => {
        const headerElement = document.querySelector('header');
        if (headerElement) {
             lucide.createIcons({ context: headerElement });
        }
    }, []);

    return (
        <header className="flex h-14 items-center gap-4 border-b border-border bg-background px-6 sticky top-0 z-30 flex-shrink-0">
            <h1 className="text-lg font-semibold text-foreground flex-1 whitespace-nowrap overflow-hidden text-ellipsis">
                Design System - Mastodon AI Bot (React) v1.6 {/* Version Bump */}
            </h1>
            <div className="flex items-center gap-2 flex-shrink-0">
                {/* Use updated muted tag style */}
                <span className="tag tag-slate">Version 1.6</span>
            </div>
        </header>
    );
}

// Footer Component
function Footer() {
     useEffect(() => {
        const footerElement = document.querySelector('footer');
        if (footerElement) {
             lucide.createIcons({ context: footerElement });
        }
    }, []);
    return (
        <footer className="flex h-8 items-center text-xs border-t border-border bg-background px-4 text-muted-foreground flex-shrink-0 z-10">
            <span>Mastodon AI Bot Design System - v1.6</span> {/* Updated Version */}
            <div className="flex-1 text-right">
                <span>React, Tailwind, Lucid, Monaco</span>
            </div>
        </footer>
    );
}

// Monaco Editor Component (Unchanged Logic)
function MonacoEditor({ code, language = 'html', editorId, height = '300px' }) {
    const editorContainerRef = useRef(null);
    const editorInstanceRef = useRef(null);

    useEffect(() => {
        let editorInstance = null;
        let requireContext = window.require || (typeof require !== 'undefined' ? require : null);

        if (editorContainerRef.current && requireContext && typeof monaco !== 'undefined') {
            // console.log(`Attempting to initialize Monaco Editor for: ${editorId}`);
            editorContainerRef.current.innerHTML = '';
            editorContainerRef.current.style.minHeight = '100px';
            editorContainerRef.current.style.height = height;

            try {
                editorInstance = monaco.editor.create(editorContainerRef.current, {
                    value: code || '',
                    language: language,
                    theme: 'vs-light', // Consider 'vs' or a custom theme matching variables
                    readOnly: true,
                    minimap: { enabled: false },
                    automaticLayout: true,
                    scrollBeyondLastLine: false,
                    wordWrap: 'on',
                    contextmenu: false,
                    fontSize: 12,
                    renderWhitespace: "none",
                    lineNumbers: "off",
                    scrollbar: { vertical: 'auto', horizontal: 'auto' }
                });
                editorInstanceRef.current = editorInstance;
                // console.log(`Monaco Editor initialized successfully for: ${editorId}`);
            } catch (error) {
                console.error(`Error creating Monaco editor for ${editorId}:`, error);
                if (editorContainerRef.current) {
                    editorContainerRef.current.textContent = 'Error loading code viewer.';
                    editorContainerRef.current.style.height = '50px';
                }
            }
        } else {
            console.warn(`Monaco prerequisites not met for ${editorId}. Container: ${!!editorContainerRef.current}, Require: ${!!requireContext}, Monaco: ${typeof monaco}`);
            if (editorContainerRef.current) {
                editorContainerRef.current.textContent = 'Loading code viewer...';
                editorContainerRef.current.style.height = '50px';
            }
        }

        return () => {
            if (editorInstanceRef.current) {
                // console.log(`Disposing Monaco Editor for: ${editorId}`);
                try { editorInstanceRef.current.dispose(); }
                catch (disposeError) { console.warn(`Error disposing Monaco editor ${editorId}:`, disposeError); }
                editorInstanceRef.current = null;
            }
            if (editorContainerRef.current) { editorContainerRef.current.innerHTML = ''; }
        };
    }, [code, language, editorId, height]);

    return <div id={editorId} ref={editorContainerRef} className="monaco-editor-container w-full border border-border rounded-md mt-4 overflow-hidden" style={{ height: height, minHeight: '100px' }}></div>;
}


// Component Preview Component (Logic Unchanged)
function ComponentPreview({ componentId, title, description, previewContent, codeContent, usageContent, codeLanguage = 'html', usageLanguage = 'html', minHeight = '200px' }) {
    const [activeTab, setActiveTab] = useState('preview');
    const uniqueCodeEditorId = `code-editor-${componentId}`;
    const uniqueUsageEditorId = `usage-editor-${componentId}`;

    useEffect(() => {
        if (activeTab === 'preview') {
            setTimeout(() => {
                const previewContainer = document.getElementById(`preview-${componentId}`);
                if (previewContainer) {
                    const iconElements = previewContainer.querySelectorAll('[data-lucide]:not([data-rendered-by-react])');
                    if (iconElements.length > 0) {
                         try { lucide.createIcons({ nodes: Array.from(iconElements) }); }
                         catch (e) { console.warn(`Lucide error in preview for ${componentId}:`, e); }
                    }
                 }
            }, 150);
        }
    }, [activeTab, componentId, previewContent]);

    return (
        <div className="mb-16" id={`components-${componentId}`}>
            <h3 className="text-xl font-semibold mt-10 mb-3 not-prose">{title}</h3>
            <p className="text-muted-foreground mb-4">{description}</p>

            {/* Tabs */}
            <div className="flex border-b border-border mb-5 mt-5">
                <button
                    onClick={() => setActiveTab('preview')}
                    className={`tab-button ${activeTab === 'preview' ? 'tab-button-active' : 'tab-button-inactive'}`}
                >
                    Preview & Usage
                </button>
                <button
                    onClick={() => setActiveTab('code')}
                    className={`tab-button ${activeTab === 'code' ? 'tab-button-active' : 'tab-button-inactive'}`}
                >
                    Component Code
                </button>
            </div>

            {/* Tab Content */}
            <div>
                {/* Preview & Usage Tab */}
                {activeTab === 'preview' && (
                    <div id={`preview-${componentId}`}>
                        <div className="card p-6 not-prose space-y-4 mb-6 border-dashed border-primary/30">
                            {previewContent}
                        </div>
                        {usageContent && (
                            <Fragment>
                                <h4 className="text-base font-medium mt-6 mb-2 text-foreground">Usage Example</h4>
                                <p className="text-sm text-muted-foreground mb-3">How to implement this component or pattern.</p>
                                <div className="not-prose">
                                    <MonacoEditor
                                        editorId={uniqueUsageEditorId}
                                        code={usageContent}
                                        language={usageLanguage}
                                        height="150px"
                                    />
                                </div>
                            </Fragment>
                        )}
                    </div>
                )}
                {/* Code Tab */}
                {activeTab === 'code' && (
                     <div className="not-prose">
                        <h4 className="text-base font-medium mb-2 text-foreground">Implementation Code</h4>
                        <p className="text-sm text-muted-foreground mb-3">The underlying HTML structure or React component code.</p>
                        <MonacoEditor
                            editorId={uniqueCodeEditorId}
                            code={codeContent}
                            language={codeLanguage}
                            height={minHeight}
                        />
                    </div>
                )}
            </div>
        </div>
    );
}


// Collapse Card Component - Updated colors, icons
function CollapseCard({ step, onToggleExpand, onOpenLlmModal }) {
    const { id, title, description, details, status, duration, icon: baseIcon, isExpanded, llmCall } = step;

    let borderStyle = 'border-border'; // Default border
    let iconName = baseIcon || 'circle-dashed';
    let iconColor = 'text-muted-foreground';
    let statusText = null;
    let statusColor = 'text-muted-foreground';
    let showLlmButton = !!llmCall;
    let isProcessing = status === 'processing';

    // Use variables for status colors
    if (status === 'complete') {
        borderStyle = 'border-l-[hsl(var(--success))]'; iconName = 'check-circle'; iconColor = 'text-success';
    } else if (isProcessing) {
        borderStyle = 'border-l-[hsl(var(--primary))]'; iconName = 'loader-2'; iconColor = 'text-primary'; statusText = 'Running...'; statusColor = 'text-primary';
    } else if (status === 'error') {
        borderStyle = 'border-l-[hsl(var(--destructive))]'; iconName = 'alert-circle'; iconColor = 'text-destructive'; statusText = 'Error'; statusColor = 'text-destructive';
    } else {
        borderStyle = 'border-l-border'; // explicit default if needed
    }

    return (
        // Removed specific color border class, using style for dynamic variable color
        <div className={`border bg-background rounded-md shadow-sm overflow-hidden border-l-4 ${borderStyle} ${isProcessing ? 'ring-1 ring-primary/20 shadow-md' : ''} ${status === 'pending' ? 'opacity-80 hover:opacity-100 transition-opacity' : ''}`}>
            <div className="flex items-center p-3 cursor-pointer hover:bg-accent/50 transition-colors" onClick={() => onToggleExpand(id)}>
                {/* Status Icon (Uses new default small size) */}
                <div className="mr-3 flex-shrink-0 pt-0.5">
                    <span className={iconColor}>
                        <Icon name={iconName} />
                    </span>
                </div>
                <div className="flex-grow">
                    <p className="font-medium text-sm text-foreground">{title}</p>
                </div>
                <div className="flex items-center ml-3 flex-shrink-0 space-x-2">
                    {duration !== null && status !== 'processing' && status !== 'pending' && (
                        <span className="text-xs text-muted-foreground">({duration}ms)</span>
                    )}
                    {statusText && (
                        <span className={`text-xs font-medium ${statusColor}`}>{statusText}</span>
                    )}
                    {showLlmButton && (
                        <button
                            onClick={(e) => { e.stopPropagation(); onOpenLlmModal(llmCall); }}
                            className="button-60 button-60-outline button-60-xs text-primary border-primary/50 hover:bg-primary/10"
                            title="View LLM Details">
                            {/* Icon size controlled by button-xs css (w-3 h-3) */}
                            <Icon name="inspect" className="mr-1" /> <span className="text-xs">LLM</span>
                        </button>
                    )}
                    <button onClick={(e) => { e.stopPropagation(); onToggleExpand(id); }} className="button-60 button-60-ghost button-60-icon-xs text-muted-foreground" title={isExpanded ? "Collapse Details" : "Expand Details"}>
                         {/* Icon size controlled by button-xs css (w-3 h-3) */}
                        <Icon name="chevron-down" className={`transition-transform duration-200 `} />
                    </button>
                </div>
            </div>

            {isExpanded && (
                <div className="border-t border-border bg-muted/30">
                    <div className="px-4 py-3 ml-7 space-y-2"> {/* Adjust ml if needed based on icon size */}
                        <p className="text-sm text-muted-foreground">{description}</p>
                        {details && (
                            <p className="text-xs text-muted-foreground mt-1 p-1.5 bg-background rounded-sm border border-border">
                                {details}
                            </p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
}


// Modal Component - Updated icons, input radius
function Modal({ isOpen, onClose, modalType, modalData }) {
    useEffect(() => {
        if (isOpen) {
            setTimeout(() => {
                 const modalContent = document.querySelector('[role="dialog"] [data-modal-content]');
                 if (modalContent) {
                    const iconsInModal = modalContent.querySelectorAll('[data-lucide]:not([data-rendered-by-react])');
                     if (iconsInModal.length > 0) {
                         try { lucide.createIcons({ nodes: Array.from(iconsInModal) }); }
                         catch(e) { console.warn("Lucide error in modal:", e); }
                     }
                 }
            }, 150);
        }
    }, [isOpen, modalType, modalData]);

    useEffect(() => {
        const handleKeyDown = (event) => { if (event.key === 'Escape') { onClose(); } };
        if (isOpen) { window.addEventListener('keydown', handleKeyDown); }
        return () => { window.removeEventListener('keydown', handleKeyDown); };
    }, [isOpen, onClose]);

    if (!isOpen) return null;

    const overlayClasses = isOpen ? 'opacity-100' : 'opacity-0';
    const panelClasses = isOpen ? 'opacity-100 scale-100' : 'opacity-0 scale-95';

    return (
        <div
            className="fixed inset-0 z-50 flex items-start justify-center pt-16 sm:pt-24 p-4 transition-opacity duration-300 ease-out"
            style={{ opacity: isOpen ? 1 : 0 }}
            role="dialog"
            aria-modal="true"
            aria-labelledby={modalType === 'llm' ? 'llm-modal-title' : 'example-modal-title'}
        >
            <div onClick={onClose} className={`fixed inset-0 bg-black/70 backdrop-blur-sm transition-opacity duration-300 ease-out ${overlayClasses}`} aria-hidden="true"></div>

            <div onClick={(e) => e.stopPropagation()} className={`relative w-full max-w-3xl bg-card rounded-lg shadow-xl overflow-hidden border border-border transform transition-all duration-300 ease-out ${panelClasses}`} data-modal-content>

                {modalType === 'llm' && (
                    <div>
                        <div className="flex items-center justify-between p-4 border-b border-border">
                            <h3 id="llm-modal-title" className="text-lg font-semibold text-foreground flex items-center">
                                {/* Default small icon */}
                                <Icon name="brain-circuit" className="mr-2 text-primary" /> LLM Call Details
                            </h3>
                            <button onClick={onClose} className="button-60 button-60-ghost button-60-icon-sm text-muted-foreground hover:bg-accent" aria-label="Close modal">
                                <Icon name="x" className="w-4 h-4" /> {/* Keep close icon slightly larger */}
                            </button>
                        </div>
                        <div className="p-6 space-y-5 max-h-[70vh] overflow-y-auto">
                            {modalData ? (
                                <div className="space-y-5">
                                    <div>
                                        <label className="block text-sm font-medium text-foreground mb-1.5">Model Used:</label>
                                        {/* Use adjusted tag style */}
                                        <span className="tag tag-purple tag-lg">
                                           <Icon name="cpu" className="w-3.5 h-3.5 mr-1.5 opacity-70" /> {modalData.modelUsed}
                                        </span>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-foreground mb-1.5">System Prompt:</label>
                                        <div className="bg-muted border border-border rounded-md p-3 shadow-inner max-h-40 overflow-y-auto">
                                            <pre className="message-blob-text !text-muted-foreground !text-xs">{modalData.systemPrompt}</pre>
                                        </div>
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-foreground mb-1.5">User Message(s):</label>
                                        {/* Use primary/10 for user message background? or keep blue */}
                                        <div className="bg-blue-50 border border-blue-200 rounded-md p-3 shadow-inner max-h-40 overflow-y-auto">
                                             <pre className="message-blob-text !text-blue-900 !text-xs">{modalData.userMessages}</pre>
                                        </div>
                                    </div>
                                     {modalData.llmResponse && (
                                        <div>
                                            <label className="block text-sm font-medium text-foreground mb-1.5">LLM Response:</label>
                                             {/* Use success/10 for response background? or keep green */}
                                            <div className="bg-green-50 border border-green-200 rounded-md p-3 shadow-inner max-h-48 overflow-y-auto">
                                                 <pre className="message-blob-text !text-green-900 !text-xs">{modalData.llmResponse}</pre>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ) : (
                                <p className="text-muted-foreground">No LLM data available.</p>
                            )}
                        </div>
                        <div className="px-6 py-3 bg-muted border-t border-border text-right">
                            <button onClick={onClose} className="button-60 button-60-secondary button-60-sm">Close</button>
                        </div>
                    </div>
                )}

                {modalType === 'example' && (
                     <div>
                        <div className="flex items-center justify-between p-4 border-b border-border">
                            <h3 id="example-modal-title" className="text-lg font-semibold text-foreground flex items-center">
                               {/* Default small icon */}
                               <Icon name="layout-panel-left" className="mr-2 text-primary" /> Example Modal
                            </h3>
                            <button onClick={onClose} className="button-60 button-60-ghost button-60-icon-sm text-muted-foreground hover:bg-accent" aria-label="Close modal">
                                <Icon name="x" className="w-4 h-4" /> {/* Keep close icon slightly larger */}
                            </button>
                        </div>
                        <div className="p-6 space-y-5 max-h-[70vh] overflow-y-auto">
                            <p className="text-muted-foreground">This is the content area of the example modal.</p>
                            <div>
                                <label htmlFor="modal-input" className="block text-sm font-medium text-foreground mb-1.5">Sample Input:</label>
                                {/* Use updated radius */}
                                <input type="text" id="modal-input" name="modal-input" className="block w-full rounded-md border-input shadow-sm focus:border-primary focus:ring-primary sm:text-sm bg-background p-2 h-9" placeholder="Enter something..." />
                            </div>
                             {/* Uses updated CheckboxSwitch styles */}
                             <CheckboxSwitch id="modal-switch" labelText="Optional Setting:" name="modal-switch" value="example"/>
                        </div>
                        <div className="px-6 py-3 bg-muted border-t border-border flex justify-end space-x-2">
                            <button onClick={onClose} className="button-60 button-60-secondary button-60-sm">Cancel</button>
                            <button onClick={onClose} className="button-60 button-60-primary button-60-sm">Confirm Action</button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

// Avatar Component - Updated size slightly, neutral placeholder
function Avatar({ src, alt, size = 'md' }) {
  const sizeClasses = {
    sm: 'h-6 w-6', // Keep small
    md: 'h-7 w-7', // UPDATED - Slightly smaller default
    lg: 'h-9 w-9', // UPDATED - Slightly smaller large
  };
   // Neutral placeholder (SVG data URI for a gray circle)
   const placeholder = 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImhzbCgyMjAsIDEzJSwgODAlKSIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PGNpcmNsZSBjeD0iMTIiIGN5PSIxMiIgcj0iMTAiLz48L3N2Zz4=';

  return (
    <img
      className={`inline-block rounded-full flex-shrink-0 bg-muted/50 ${sizeClasses[size] || sizeClasses['md']}`} // Added bg-muted for placeholder visibility
      src={src || placeholder}
      alt={alt || 'User Avatar'}
      // Add error handling to fall back to placeholder if src fails to load
      onError={(e) => { if (e.target.src !== placeholder) { e.target.onerror = null; e.target.src = placeholder; } }}
    />
  );
}

// --- Checkbox Switch Component (Uses updated CSS) ---
function CheckboxSwitch({ id, labelText, offText = "Off", onText = "On", ...props }) {
    const uniqueId = id || `switch-${Math.random().toString(36).substring(7)}`;
    return (
        <div className="checkbox-wrapper-35">
            <input className="switch" type="checkbox" id={uniqueId} {...props} />
            <label htmlFor={uniqueId}>
                {labelText && <span className="switch-x-text">{labelText}</span>}
                <span className="switch-x-toggletext">
                    <span className="switch-x-unchecked">
                        <span className="switch-x-hiddenlabel">Unchecked: </span>{offText}
                    </span>
                    <span className="switch-x-checked">
                        <span className="switch-x-hiddenlabel">Checked: </span>{onText}
                    </span>
                </span>
            </label>
        </div>
    );
}


// Main Content Area Component
function MainContent({ onOpenModal }) {
     // State for Collapse Card example
    const [steps, setSteps] = useState([
        { id: 1, title: 'Analyzing Prompt', description: 'Identifying keywords, entities, and overall intent.', details: 'Intent: Generate Toot, Tags: #AI, #Mastodon', status: 'complete', duration: 650, icon: 'scan-text', isExpanded: false, llmCall: null },
        { id: 2, title: 'Retrieving Context (Optional)', description: 'Fetching relevant previous posts or external info.', details: 'No relevant context found.', status: 'complete', duration: 150, icon: 'database', isExpanded: false, llmCall: null },
        { id: 3, title: 'Content Generation (LLM Call)', description: 'Generating draft based on prompt and retrieved data.', details: 'Using Llama 3 Instruct model with creative parameters.', status: 'processing', duration: null, icon: 'brain-circuit', isExpanded: true, llmCall: { modelUsed: 'llama3-70b-instruct', systemPrompt: 'You are a helpful AI assistant designed to generate Mastodon posts (toots). Be concise, engaging, and use relevant hashtags. Max length 500 chars.', userMessages: 'Draft a short, engaging toot about the recent advancements in open-source AI models. Mention potential benefits for the Mastodon community.', llmResponse: "Exciting times for open-source AI! 🚀 Recent models offer more transparency & community control. Great potential for cool tools and bots right here on the Fediverse! What benefits do you see?\n\n#OpenSourceAI #AI #Fediverse #Mastodon" } },
        { id: 4, title: 'Formatting Output', description: 'Ensuring toot structure and length limits.', details: 'Character count: 250. Hashtags: 4.', status: 'pending', duration: null, icon: 'pilcrow', isExpanded: false, llmCall: null },
        { id: 5, title: 'Safety & Quality Check', description: 'Running checks for harmful content and coherence.', details: '', status: 'pending', duration: null, icon: 'shield-check', isExpanded: false, llmCall: null },
    ]);

    const handleToggleExpand = (stepId) => {
        setSteps(prevSteps =>
            prevSteps.map(step =>
                step.id === stepId ? { ...step, isExpanded: !step.isExpanded } : step
            )
        );
    };

    const handleOpenLlmModal = (llmData) => {
        onOpenModal('llm', llmData);
    };

    // Render initial icons for static content
    useEffect(() => {
        const mainElement = document.getElementById('main-scroll-area');
        if (mainElement) {
             const staticIcons = mainElement.querySelectorAll('section > h2 [data-lucide]');
             if (staticIcons.length > 0) {
                 try { lucide.createIcons({ nodes: Array.from(staticIcons) }); }
                 catch(e) { console.warn("Lucide error in MainContent headings:", e); }
             }
        }
    }, []);

    // --- Component Preview Data ---

    // BUTTON PREVIEW - UPDATED Icons/Sizes
    const buttonPreview = (
        <Fragment>
            <h4 className="text-base font-medium mb-3">Variants & Sizes</h4>
            <div className="flex flex-wrap gap-3 items-center mb-3">
                <button className="button-60 button-60-primary">Primary</button>
                <button className="button-60 button-60-secondary">Secondary</button>
                <button className="button-60 button-60-outline">Outline</button>
                <button className="button-60 button-60-ghost">Ghost</button>
                <button className="button-60 button-60-destructive">Destructive</button>
                <button className="button-60 button-60-primary" disabled>Disabled</button>
            </div>
            <div className="flex flex-wrap gap-3 items-center mb-3">
                <button className="button-60 button-60-primary button-60-sm">Primary SM</button>
                <button className="button-60 button-60-secondary button-60-sm">Secondary SM</button>
                <button className="button-60 button-60-outline button-60-sm">Outline SM</button>
                <button className="button-60 button-60-secondary button-60-sm" disabled>Disabled SM</button>
            </div>
            <div className="flex flex-wrap gap-3 items-center">
                <button className="button-60 button-60-primary button-60-xs">Primary XS</button>
                <button className="button-60 button-60-secondary button-60-xs">Secondary XS</button>
                <button className="button-60 button-60-outline button-60-xs">Outline XS</button>
                <button className="button-60 button-60-outline button-60-xs" disabled>Disabled XS</button>
            </div>

            <h4 className="text-base font-medium mt-6 mb-3">With Icons</h4>
            <div className="flex flex-wrap gap-3 items-center">
                {/* Icons are smaller (w-3/h-3 in sm button) */}
                <button className="button-60 button-60-primary button-60-sm"><Icon name="plus" /> Add Item</button>
                <button className="button-60 button-60-outline button-60-sm"><Icon name="play" /> Run Again</button>
                <button className="button-60 button-60-secondary button-60-sm"><Icon name="loader-2"/> Processing...</button>
                <button className="button-60 button-60-ghost button-60-sm text-destructive"><Icon name="trash-2" /> Delete</button>
            </div>

            <h4 className="text-base font-medium mt-6 mb-3">Icon Buttons</h4>
            <div className="flex flex-wrap gap-3 items-center">
                {/* Icons are smaller (w-3.5 default, w-3 sm, w-3 xs) */}
                <button className="button-60 button-60-primary button-60-icon"><Icon name="plus" /></button>
                <button className="button-60 button-60-outline button-60-icon-sm"><Icon name="trash-2" /></button>
                <button className="button-60 button-60-ghost button-60-icon-xs"><Icon name="settings" /></button>
                <button className="button-60 button-60-secondary button-60-icon-sm" disabled><Icon name="copy" /></button>
            </div>
        </Fragment>
    );
    const buttonCode = `<!-- Base Button (Uses text-sm, h-9, rounded-md) -->
<button class="button-60" role="button">Button Text</button>

<!-- Variants -->
<button class="button-60 button-60-primary">Primary</button>
<button class="button-60 button-60-secondary">Secondary</button>
<button class="button-60 button-60-outline">Outline</button>
<button class="button-60 button-60-ghost">Ghost</button>
<button class="button-60 button-60-destructive">Destructive</button>

<!-- Sizes -->
<button class="button-60 button-60-primary button-60-sm">Small (h-8)</button>
<button class="button-60 button-60-primary button-60-xs">Extra Small (h-7)</button>

<!-- Disabled -->
<button class="button-60 button-60-primary" disabled>Disabled</button>

<!-- With Icon (Icon size w-3.5, w-3, w-3 based on button size) -->
<button class="button-60 button-60-primary button-60-sm">
  <Icon name="plus" /> Add Item
</button>

<!-- Icon Button -->
<button class="button-60 button-60-outline button-60-icon-sm">
  <Icon name="trash-2" />
</button>`;
    const buttonUsage = `// Use 'button-60' and add variant/size classes.
// Variants: -primary, -secondary, -outline, -ghost, -destructive
// Sizes: -sm, -xs (default is like md)
// Icon Buttons: -icon, -icon-sm, -icon-xs
// CSS handles icon sizing and spacing based on button class.

<button className="button-60 button-60-primary">
    <Icon name="save" /> Save
</button>

<button className="button-60 button-60-ghost button-60-icon-xs">
    <Icon name="settings" />
</button>`;

    // CARD PREVIEW - Uses updated buttons
    const cardPreview = (
        <Fragment>
            <h4 className="text-base font-medium mb-4">Standard Card</h4>
            <div className="card max-w-md"> {/* rounded-lg */}
                <div className="p-6">
                    <h3 className="text-lg font-semibold text-card-foreground mb-1">Card Title</h3>
                    <p className="text-sm text-muted-foreground">Card content area with <code>p-6</code> padding.</p>
                </div>
                <div className="p-4 bg-muted/50 border-t border-border flex justify-end space-x-2">
                     {/* Buttons use updated styles */}
                     <button className="button-60 button-60-secondary button-60-sm">Cancel</button>
                     <button className="button-60 button-60-primary button-60-sm">Confirm</button>
                </div>
            </div>

             <h4 className="text-base font-medium mt-6 mb-4">Card without Footer</h4>
             <div className="card max-w-md p-6">
                 <div className="flex items-center space-x-3">
                     {/* Icon container uses rounded-md */}
                    <span className="flex items-center justify-center h-8 w-8 rounded-md bg-primary/10 text-primary">
                        <Icon name="info"/> {/* Default small icon */}
                    </span>
                    <div>
                         <h3 className="text-md font-medium text-card-foreground">Informational Card</h3>
                        <p className="text-sm text-muted-foreground">Content directly inside.</p>
                    </div>
                 </div>
            </div>
        </Fragment>
    );
    const cardCode = `<!-- Standard Card (rounded-lg) -->
<div class="card max-w-md">
  <div class="p-6">...</div>
  <div class="p-4 bg-muted/50 border-t flex justify-end space-x-2">
     {/* Uses updated button styles (rounded-md) */}
     <button class="button-60 button-60-secondary button-60-sm">Cancel</button>
     <button class="button-60 button-60-primary button-60-sm">Confirm</button>
  </div>
</div>

<!-- Simple Card (Content only) -->
<div class="card max-w-md p-6">...</div>`;
    const cardUsage = `<div class="card {max-width} {padding}">
  {/* Optional Header/Content/Footer */}
  <div class="p-4 bg-muted/50 border-t flex justify-end space-x-2">
    <button class="button-60 button-60-secondary button-60-sm">...</button>
    <button class="button-60 button-60-primary button-60-sm">...</button>
  </div>
</div>`;

    // TAG PREVIEW - Updated colors and icons
     const tagPreview = (
         <Fragment>
            <h4 className="text-base font-medium mb-4">Category Tags (Muted)</h4>
            <div className="flex flex-wrap gap-2 items-center mb-3">
                <span className="tag tag-blue">#AI</span>
                <span className="tag tag-green">#Mastodon</span>
                <span className="tag tag-purple">#OpenSource</span>
                <span className="tag tag-slate">Keyword</span> {/* Slate is good neutral */}
            </div>
             <h4 className="text-base font-medium mb-4">Status Indicators</h4>
            <div className="flex flex-wrap gap-2 items-center">
                {/* Icons are smaller (w-3 h-3) */}
                 <span className="tag tag-yellow"><Icon name="loader-2" className="w-3 h-3 mr-1 "/> Processing</span>
                 {/* Use variable-based success tag */}
                 <span className="tag tag-success"><Icon name="check-circle" className="w-3 h-3 mr-1"/> Complete</span>
                 <span className="tag tag-slate"><Icon name="circle-dashed" className="w-3 h-3 mr-1"/> Pending</span>
                 {/* Use variable-based destructive tag */}
                <span className="tag tag-destructive"><Icon name="alert-circle" className="w-3 h-3 mr-1"/> Error</span>
                 <span className="tag tag-purple tag-lg"><Icon name="cpu" className="w-3.5 h-3.5 mr-1.5"/> llama3-70b</span> {/* Larger tag uses slightly larger icon */}
            </div>
        </Fragment>
    );
    const tagCode = `<!-- Base Tag (rounded-full, text-xs) -->
<span class="tag {color-classes}"> Tag Text </span>

<!-- Larger Tag (rounded-md, text-sm) -->
<span class="tag tag-lg {color-classes}"> Larger Tag </span>

<!-- Tag with Icon (Icon generally w-3 h-3) -->
<span class="tag {color-classes}">
  <Icon name="{icon-name}" className="w-3 h-3 mr-1" /> Status
</span>

<!-- Color Examples (Muted Tailwind) -->
<span class="tag bg-blue-50 text-blue-700">#AI</span>
<span class="tag bg-slate-100 text-slate-700">Keyword</span>

<!-- Color Examples (CSS Variables) -->
<span class="tag tag-success"><Icon name="check-circle" class="w-3 h-3 mr-1"/>Complete</span>
<span class="tag tag-destructive"><Icon name="alert-circle" class="w-3 h-3 mr-1"/>Error</span>`;
    const tagUsage = `// Predefined classes: tag-blue, tag-green, tag-purple, tag-gray, tag-yellow, tag-teal, tag-slate, tag-red
// Variable classes: tag-primary, tag-muted, tag-destructive, tag-success
<span class="tag tag-slate">
  <Icon name="info" className="w-3 h-3 mr-1" /> Info
</span>`;

    // TABLE PREVIEW - Updated buttons/icons
    const tablePreview = (
         <Fragment>
            <h4 className="text-base font-medium mb-4">Standard Table</h4>
            <div className="overflow-x-auto border border-border rounded-lg">
                <table className="min-w-full text-sm divide-y divide-border">
                    <thead className="bg-muted/50">
                        <tr>
                            <th scope="col" className="py-2 px-3 text-left font-medium text-muted-foreground">ID</th>
                            <th scope="col" className="py-2 px-3 text-left font-medium text-muted-foreground">Name</th>
                            <th scope="col" className="py-2 px-3 text-left font-medium text-muted-foreground">Status</th>
                            <th scope="col" className="py-2 px-3 text-left font-medium text-muted-foreground">Actions</th>
                        </tr>
                    </thead>
                    <tbody className="bg-background divide-y divide-border">
                        <tr>
                            <td className="py-2 px-3 whitespace-nowrap font-mono text-xs">a1b2c3d4</td>
                            <td className="py-2 px-3">Item One</td>
                            {/* Use success tag */}
                            <td className="py-2 px-3"><span className="tag tag-success">Active</span></td>
                            <td className="py-2 px-3 space-x-1">
                                {/* Buttons use updated styles (xs, ghost, icon-xs -> w-3 h-3 icon) */}
                                <button className="button-60 button-60-ghost button-60-icon-xs"><Icon name="edit-3" /></button>
                                <button className="button-60 button-60-ghost button-60-icon-xs text-destructive"><Icon name="trash-2" /></button>
                            </td>
                        </tr>
                        <tr>
                            <td className="py-2 px-3 whitespace-nowrap font-mono text-xs">e5f6g7h8</td>
                            <td className="py-2 px-3">Item Two</td>
                            <td className="py-2 px-3"><span className="tag tag-slate">Inactive</span></td>
                             <td className="py-2 px-3 space-x-1">
                                <button className="button-60 button-60-ghost button-60-icon-xs"><Icon name="edit-3" /></button>
                                <button className="button-60 button-60-ghost button-60-icon-xs text-destructive"><Icon name="trash-2" /></button>
                            </td>
                        </tr>
                        <tr>
                            <td className="py-2 px-3 whitespace-nowrap font-mono text-xs">i9j0k1l2</td>
                            <td className="py-2 px-3">Item Three</td>
                             <td className="py-2 px-3"><span className="tag tag-yellow">Pending</span></td>
                             <td className="py-2 px-3 space-x-1">
                                <button className="button-60 button-60-ghost button-60-icon-xs"><Icon name="edit-3" /></button>
                                <button className="button-60 button-60-ghost button-60-icon-xs text-destructive"><Icon name="trash-2" /></button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </Fragment>
    );
    const tableCode = `<div class="overflow-x-auto border border-border rounded-lg">
  <table class="min-w-full text-sm divide-y divide-border">
    <thead class="bg-muted/50"> ... </thead>
    <tbody class="bg-background divide-y divide-border">
        <tr>
            <td>...</td>
            {/* Use variable tag */}
            <td><span class="tag tag-success">Active</span></td>
            <td class="py-2 px-3 space-x-1">
                {/* Action Buttons (xs) */}
                <button class="button-60 button-60-ghost button-60-icon-xs"> <Icon name="edit-3" /> </button>
                <button class="button-60 button-60-ghost button-60-icon-xs text-destructive"> <Icon name="trash-2" /> </button>
            </td>
        </tr>
    </tbody>
  </table>
</div>`;
    const tableUsage = `<div class="overflow-x-auto border rounded-lg">
  <table class="min-w-full text-sm divide-y">...</table>
</div>`;

    // COLLAPSE CARD PREVIEW - Uses updated CollapseCard
    const collapsePreview = (
        <Fragment>
            <h4 className="text-base font-medium mb-4">Interactive Sequence Example</h4>
            <div className="space-y-2">
                {steps.map(step => (
                    <CollapseCard
                        key={step.id}
                        step={step}
                        onToggleExpand={handleToggleExpand}
                        onOpenLlmModal={handleOpenLlmModal}
                    />
                ))}
             </div>
        </Fragment>
    );
    const collapseCode = `// React Component (CollapseCard) - Simplified
function CollapseCard({ step, onToggleExpand, onOpenLlmModal }) {
    // ... status logic using --success, --destructive, --primary vars ...
    // Uses Icon component (default small size)
    // Uses button-60 with -xs size for actions

    return (
        <div className="border rounded-md border-l-4 {borderStyle} ...">
            <div className="flex items-center p-3 ...">
                <Icon name={iconName}  />
                <p>{title}</p>
                <div className="flex items-center ml-3 space-x-2">
                    {/* ... duration / status ... */}
                    <button className="button-60 button-60-outline button-60-xs ...">...</button>
                    <button className="button-60 button-60-ghost button-60-icon-xs ...">...</button>
                </div>
            </div>
            {isExpanded && ( <div className="border-t p-4 ml-7 ...">...</div> )}
        </div>
    );
}`;
    const collapseUsage = `// Parent manages 'steps' array state.
// Each step: id, title, description, status ('complete', 'processing', 'error', 'pending'), isExpanded, icon, llmCall, etc.
// Status drives the left border color via CSS variables (--success, --primary, --destructive).

<div class="space-y-2">
  {steps.map(step => <CollapseCard key={step.id} ... />)}
</div>`;

    // MODAL PREVIEW - Uses updated Modal component
    const modalPreview = (
        <Fragment>
            <h4 className="text-base font-medium mb-4">Interactive Examples</h4>
             <div className="flex flex-wrap gap-3 items-center">
                <button onClick={() => onOpenModal('example', null)} className="button-60 button-60-primary button-60-sm">
                    <Icon name="layout-panel-left" /> Open Example Modal
                </button>
                <button
                    onClick={() => onOpenModal('llm', { modelUsed: 'demo-model-button', systemPrompt: 'System prompt triggered from button click.', userMessages: 'User message for button demo.', llmResponse: 'This is a simulated LLM response shown in the modal.' })}
                    className="button-60 button-60-secondary button-60-sm">
                     <Icon name="brain-circuit" /> Open LLM Modal (Demo)
                 </button>
             </div>
            <p className="text-xs text-muted-foreground mt-2">Requires state management (isOpen, type, data) in parent.</p>
        </Fragment>
    );
    const modalCode = `// React Component (Modal) - Simplified
function Modal({ isOpen, onClose, modalType, modalData }) {
    // ... effects ...
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex ..." role="dialog">
            <div onClick={onClose} className="fixed inset-0 bg-black/70 ..."></div> {/* Darker overlay */}
            <div className="relative bg-card rounded-lg ..." data-modal-content>
                {/* Header with smaller icons (w-3.5 default, w-4 close) */}
                <div className="flex justify-between p-4 border-b">...</div>
                {/* Body */}
                <div className="p-6 overflow-y-auto">
                     {/* Example Content with CheckboxSwitch (updated styles) */}
                     <CheckboxSwitch id="modal-check" labelText="Option:"/>
                     {/* Input uses rounded-md */}
                     <input type="text" class="... rounded-md ..."/>
                </div>
                {/* Footer with updated buttons */}
                <div className="px-6 py-3 bg-muted border-t text-right space-x-2">...</div>
            </div>
        </div>
    );
}`;
    const modalUsage = `// 1. Manage state (isModalOpen, modalType, modalData) in parent.
// 2. Create open/close handlers in parent.
// 3. Pass onOpenModal to triggers, render <Modal> with state & onClose.

<button onClick={() => props.onOpenModal('llm', { ... })}
        className="button-60 button-60-secondary button-60-sm">
  Show LLM Details
</button>`;

    // RESPONSE PANEL PREVIEW - Updated colors, icons, shadows
    const tweetPreview = (
        <Fragment>
            <h4 className="text-base font-medium mb-4">Example Generated Response Panel</h4>
            {/* Success State Example - Use Success Variable */}
            <div className="p-4 border border-[hsl(var(--success))] rounded-lg bg-[hsl(var(--success)/0.08)] ring-1 ring-[hsl(var(--success)/0.15)] shadow-sm">
                <div className="flex flex-wrap justify-between items-center gap-2 mb-3">
                    <h3 className="text-base font-semibold text-success flex items-center">
                        {/* Icon slightly larger, use success color */}
                        <Icon name="check-check" className="w-4 h-4 mr-2"/> Response Generated
                    </h3>
                    <span className="text-xs text-success/90 font-medium">Total time: 1234ms</span>
                </div>
                <div className="p-3 bg-background border border-border rounded-md shadow-inner mb-4">
                    <p className="text-sm text-foreground whitespace-pre-wrap">Exciting times for open-source AI! 🚀 Recent models offer more transparency & community control. Great potential for cool tools and bots right here on the Fediverse! What benefits do you see?{'\n\n'}#OpenSourceAI #AI #Fediverse #Mastodon</p>
                </div>
                <div className="pt-3 border-t border-[hsl(var(--success)/0.3)] flex flex-wrap gap-2 items-center justify-between">
                    <div className="flex flex-wrap gap-2 items-center">
                         {/* Buttons use updated styles/icons */}
                        <button className="button-60 button-60-primary button-60-sm"><Icon name="send"/> Post</button>
                        <button className="button-60 button-60-outline button-60-sm"><Icon name="copy"/> Copy</button>
                        <button className="button-60 button-60-ghost button-60-sm text-muted-foreground"><Icon name="edit-3"/> Edit</button>
                    </div>
                    <button className="button-60 button-60-outline button-60-sm text-muted-foreground hover:text-primary border-primary/20 hover:border-primary/40 hover:bg-primary/10">
                        <Icon name="refresh-ccw"/> Regenerate
                    </button>
                </div>
            </div>
             {/* Error State Example - Use Destructive Variable */}
             <h4 className="text-base font-medium mt-6 mb-4">Example Error Panel</h4>
             <div className="mt-4 p-4 border border-[hsl(var(--destructive))] rounded-lg bg-[hsl(var(--destructive)/0.08)] ring-1 ring-[hsl(var(--destructive)/0.15)] shadow-sm">
                <div className="flex justify-between items-center mb-3">
                    <h3 className="text-base font-semibold text-destructive flex items-center">
                         {/* Icon slightly larger, use destructive color */}
                        <Icon name="alert-triangle" className="w-4 h-4 mr-2"/> Generation Failed
                    </h3>
                     <span className="text-xs text-destructive/90 font-medium">Error Code: 500</span>
                </div>
                <div className="p-3 bg-background border border-border rounded-md shadow-inner mb-4">
                     <p className="text-sm text-destructive">{/* Error message using text-destructive */}</p>
                 </div>
                 <div className="pt-3 border-t border-[hsl(var(--destructive)/0.3)] flex flex-wrap gap-2 items-center justify-end">
                    <button className="button-60 button-60-outline button-60-sm text-muted-foreground hover:text-primary border-primary/20 hover:border-primary/40 hover:bg-primary/10">
                         <Icon name="refresh-ccw"/> Try Again
                    </button>
                 </div>
            </div>
        </Fragment>
    );
    const tweetCode = `<!-- Success State Example (Using --success variable) -->
<div class="p-4 border border-[hsl(var(--success))] rounded-lg bg-[hsl(var(--success)/0.08)] ... shadow-sm">
    <div class="flex justify-between mb-3">
        <h3 class="text-base font-semibold text-success flex items-center">
            <Icon name="check-check" class="w-4 h-4 mr-2"/> Response Generated
        </h3> ...
    </div>
    <div class="p-3 bg-background border rounded-md shadow-inner mb-4"> ... </div>
    <div class="pt-3 border-t border-[hsl(var(--success)/0.3)] flex ...">
         {/* Updated Buttons */}
         <button class="button-60 button-60-primary button-60-sm">...</button>
         ...
    </div>
</div>

<!-- Error State Example (Using --destructive variable) -->`;
    const tweetUsage = `// Layout uses Flexbox, Padding, Borders.
// Use CSS Variables for dynamic colors based on state (success/error).
// --success, --success-foreground
// --destructive, --destructive-foreground
// Use Button components with updated styles.

<div className={\`p-4 border rounded-lg shadow-sm \${isSuccess ? 'border-[hsl(var(--success))] bg-[hsl(var(--success)/0.08)]' : 'border-[hsl(var(--destructive))] bg-[hsl(var(--destructive)/0.08)]'}\`}>
    <h3 className={\`text-base font-semibold flex items-center \${isSuccess ? 'text-success' : 'text-destructive'}\`}>...</h3>
    {/* ... content, actions ... */}
</div>`;

    // METADATA PREVIEW - Updated icons, tags
     const metadataPreview = (
         <Fragment>
            <h4 className="text-base font-medium mb-4">Standard Metadata Block</h4>
            <div className="space-y-3 pt-2">
                <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Metadata</h3>
                <div className="text-sm text-muted-foreground space-y-2 border border-border rounded-lg p-4 bg-background/50 shadow-sm">
                    <div className="flex items-start sm:items-center">
                         {/* Default small icon */}
                        <Icon name="tag" className="mr-2 mt-0.5 sm:mt-0 flex-shrink-0 text-muted-foreground"/>
                        <span className="font-medium text-foreground/90 w-20 flex-shrink-0">Tags:</span>
                        <span className="ml-2 flex flex-wrap gap-1.5">
                             {/* Use muted tags */}
                             <span className="tag tag-blue">#AI</span>
                             <span className="tag tag-green">#Mastodon</span>
                             <span className="tag tag-purple">#OpenSource</span>
                        </span>
                    </div>
                    <div className="flex items-center">
                        <Icon name="zap" className="mr-2 flex-shrink-0 text-muted-foreground"/>
                         <span className="font-medium text-foreground/90 w-20 flex-shrink-0">Intent:</span>
                        <span className="ml-2 font-medium text-foreground">Generate Toot</span>
                    </div>
                    <div className="flex items-center">
                         <Icon name="settings-2" className="mr-2 flex-shrink-0 text-muted-foreground"/>
                        <span className="font-medium text-foreground/90 w-20 flex-shrink-0">Model:</span>
                        <span className="ml-2 font-medium text-foreground">Default Creative</span>
                    </div>
                    <div className="flex items-center">
                         <Icon name="calendar-clock" className="mr-2 flex-shrink-0 text-muted-foreground"/>
                         <span className="font-medium text-foreground/90 w-20 flex-shrink-0">Requested:</span>
                        <span className="ml-2 font-medium text-foreground">11/15/2023, 10:30 AM</span>
                    </div>
                </div>
            </div>
        </Fragment>
    );
     const metadataCode = `<div class="space-y-3 pt-2">
    <h3 class="text-xs ...">Metadata</h3>
    <div class="text-sm space-y-2 border rounded-lg p-4 ...">
        <div class="flex items-start sm:items-center">
            <Icon name="tag" class="mr-2 ..."/> {/* Uses default small size */}
            <span class="font-medium w-20 ...">Tags:</span>
            <span class="ml-2 flex flex-wrap gap-1.5">
                <span class="tag tag-blue">#AI</span> {/* Uses muted tag colors */}
            </span>
        </div>
        ...
    </div>
</div>`;
    const metadataUsage = `// Use Flexbox to align icon, key, value.
// Standardize text styles (text-sm, font-medium, text-muted-foreground).
// Use Icon component (default small size).
// Use Tag components (muted colors).

<div class="flex items-center text-sm">
  <Icon name="info" class="mr-2 flex-shrink-0 text-muted-foreground"/>
  <span class="font-medium text-foreground/90 w-20">Key:</span>
  <span class="ml-2 text-foreground">Value</span>
</div>`;

    // AVATAR PREVIEW - Updated sizes
    const avatarPreview = (
        <Fragment>
            <h4 className="text-base font-medium mb-4">Examples</h4>
            <div className="flex items-center space-x-4">
                <Avatar src="https://via.placeholder.com/48/cccccc/FFFFFF?text=U" alt="User Avatar SM" size="sm" /> {/* h-6 w-6 */}
                <Avatar src="https://via.placeholder.com/96/3b82f6/FFFFFF?text=U" alt="User Avatar MD" size="md" /> {/* h-7 w-7 */}
                <Avatar src="https://via.placeholder.com/128/10b981/FFFFFF?text=U" alt="User Avatar LG" size="lg" /> {/* h-9 w-9 */}
                <Avatar alt="Default Avatar MD" size="md" /> {/* Default placeholder h-7 w-7 */}
            </div>
             <p className="text-xs text-muted-foreground mt-3">Sizes: sm (h-6), md (h-7), lg (h-9). Uses neutral fallback.</p>
        </Fragment>
    );
    const avatarCode = `// --- React Component ---
function Avatar({ src, alt, size = 'md' }) {
  const sizeClasses = { sm: 'h-6 w-6', md: 'h-7 w-7', lg: 'h-9 w-9' }; // Updated sizes
  const placeholder = 'data:image/svg+xml;base64,...(neutral placeholder)...';

  return (
    <img
      className={\`inline-block rounded-full ... \${sizeClasses[size] || sizeClasses['md']}\`}
      src={src || placeholder} alt={alt || 'User Avatar'}
      onError={(e) => { /* fallback to placeholder */ }}
    />
  );
}`;
    const avatarUsage = `// React:
<Avatar src={userData.avatarUrl} alt="..." size="md" /> // md is h-7 w-7

// HTML:
<img class="inline-block rounded-full h-7 w-7 bg-muted/50" src="..." alt="..." />`;

    // USER INFO BLOCK PREVIEW - Updated avatar size, button icon size
    const userInfoPreview = (
         <Fragment>
            <h4 className="text-base font-medium mb-4">Example Layout</h4>
             <div className="flex items-start space-x-3 p-4 border border-border rounded-lg bg-background">
                {/* Avatar uses updated default size 'md' (h-7 w-7) */}
                <Avatar src="https://media.khiar.net/cache/accounts/avatars/114/280/126/567/340/828/original/f20936bb6bd8d8de.png" alt="UserX Avatar" size="md"/>
                <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-foreground truncate">User Display Name</p>
                    <p className="text-xs text-muted-foreground truncate">@username@instance.tld · 5m ago</p>
                </div>
                 {/* Button uses xs size, icon is w-3 h-3 */}
                <button className="button-60 button-60-ghost button-60-icon-xs text-muted-foreground flex-shrink-0">
                    <Icon name="more-vertical" />
                </button>
            </div>
        </Fragment>
    );
    const userInfoCode = `<div class="flex items-start space-x-3 p-4 border rounded-lg bg-background">
  {/* Avatar size md (h-7 w-7) */}
  <Avatar src="..." alt="..." size="md"/>
  <div class="flex-1 min-w-0"> ... </div>
  {/* Button size xs (icon w-3 h-3) */}
  <button class="button-60 button-60-ghost button-60-icon-xs ...">
    <Icon name="more-vertical" />
  </button>
</div>`;
    const userInfoUsage = `// Combine Avatar (md: h-7), text elements, Button (xs: icon h-3).
// Use Flexbox, padding, text styles, truncation.`;

    // BLOCKQUOTE PREVIEW - Uses updated prose/variable styles
    const blockquotePreview = (
        <Fragment>
             <h4 className="text-base font-medium mb-4">Standard Blockquote</h4>
             {/* Uses updated prose blockquote style with CSS vars */}
             <blockquote className="my-4">
                This is the standard style via <code>prose blockquote</code>. It uses CSS variables for border and background.
             </blockquote>
              <h4 className="text-base font-medium mb-4">Muted/Styled Blockquote</h4>
              {/* Uses utility classes to override */}
             <blockquote className="border-l-4 border-blue-300 pl-4 text-blue-800/90 text-sm py-2 bg-blue-50 rounded-r-md shadow-sm my-4 italic">
                This is a variation using direct utility classes (Tailwind colors).
             </blockquote>
        </Fragment>
    );
    const blockquoteCode = `<!-- Standard Blockquote (relies on updated prose base styles using CSS vars) -->
<blockquote class="my-4">
  Standard quoted text.
</blockquote>

<!-- Muted/Informational Variant (Uses utility classes) -->
<blockquote class="border-l-4 border-blue-300 pl-4 text-blue-800/90 text-sm py-2 bg-blue-50 rounded-r-md shadow-sm my-4 italic">
  Informational note.
</blockquote>`;
    const blockquoteUsage = `// Use standard <blockquote> for prose content.
// For styled variations, apply utility classes directly.`;

    // --- CHECKBOX SWITCH PREVIEW (Uses updated CSS) ---
    const checkboxPreview = (
        <Fragment>
            <h4 className="text-base font-medium mb-4">Interactive Examples</h4>
            <div className="space-y-3">
                <CheckboxSwitch id="switch1" labelText="Setting One:" name="setting1"/>
                <CheckboxSwitch id="switch2" labelText="Enable Feature:" name="setting2" defaultChecked />
                <CheckboxSwitch id="switch3" name="setting3" offText="Private" onText="Public"/>
                <CheckboxSwitch id="switch4" labelText="Disabled Off:" name="setting4" disabled />
                <CheckboxSwitch id="switch5" labelText="Disabled On:" name="setting5" defaultChecked disabled />
            </div>
        </Fragment>
    );
    const checkboxCode = `<!-- HTML Structure -->
<div class="checkbox-wrapper-35">
  <input class="switch" type="checkbox" id="{unique-id}" ...>
  <label for="{unique-id}"> ... </label>
</div>

/* --- CSS (Uses updated variables, rounded-full) --- */
/* .checkbox-wrapper-35 ... { ... } */

/* --- React Component Wrapper --- */
function CheckboxSwitch({ id, labelText, ... }) { ... }`;
    const checkboxUsage = `// 1. Ensure CSS for '.checkbox-wrapper-35' is included.
// 2. Use HTML or React component.
// 3. Match input 'id' and label 'htmlFor'.
<CheckboxSwitch id="notify" name="notify" labelText="Notifications:" />`;

    // --- MESSAGE BOX PREVIEW (Updated avatar, radius, shadow) ---
     const messageBoxPreview = (
        <Fragment>
            <h4 className="text-base font-medium mb-4">Chat Interface Example</h4>
            <div className="border border-border rounded-lg max-w-lg mx-auto bg-background shadow-md">
                <div className="flex flex-col space-y-4 p-4 h-96 overflow-y-auto">
                    {/* User Message */}
                    <div className="flex gap-3 justify-end">
                        <div className="order-1 max-w-[85%] flex-1 sm:max-w-[75%]">
                             {/* Bubble uses rounded-lg, shadow-sm */}
                             <div className="rounded-lg p-2.5 text-sm break-words whitespace-pre-wrap bg-primary text-primary-foreground shadow-sm">
                                Hello! Can you help me?
                             </div>
                        </div>
                    </div>
                     {/* AI Message */}
                    <div className="flex gap-2.5 justify-start items-start">
                         {/* Avatar uses sm size (h-6 w-6) */}
                        <Avatar size="sm" alt="AI Avatar" className="mt-0.5"/>
                        <div className="max-w-[85%] flex-1 sm:max-w-[75%]">
                             {/* Bubble uses rounded-lg, shadow-sm */}
                             <div className="rounded-lg p-2.5 text-sm break-words whitespace-pre-wrap bg-secondary text-secondary-foreground shadow-sm">
                                Of course! What's up?
                             </div>
                        </div>
                    </div>
                    {/* AI Message with Code */}
                    <div className="flex gap-2.5 justify-start items-start">
                        <Avatar size="sm" alt="AI Avatar" className="mt-0.5"/>
                        <div className="max-w-[85%] flex-1 sm:max-w-[75%]">
                             <div className="rounded-lg p-2.5 text-sm break-words whitespace-pre-wrap bg-secondary text-secondary-foreground shadow-sm prose prose-sm max-w-none">
                                <p>Here's some code:</p>
                                {/* Prose adds margins, use max-w-none if needed */}
                                <pre className="my-1"><code className="language-css">{`.container {\n  display: grid;\n}`}</code></pre>
                                <p>Any questions?</p>
                             </div>
                        </div>
                    </div>
                     <div className="h-[1px] w-full flex-shrink-0" aria-hidden="true"></div>
                </div>
                {/* Input Area uses rounded-md */}
                <div className="p-2 border-t border-border bg-muted/50">
                     <input type="text" placeholder="Type your message..." className="w-full text-sm rounded-md border-input p-2 h-9 focus:ring-primary focus:border-primary bg-background" />
                </div>
            </div>
        </Fragment>
    );
    const messageBoxCode = `<!-- Message Container -->
<div class="flex flex-col space-y-4 p-4 h-96 overflow-y-auto">

  {/* User Message (Right Aligned) */}
  <div class="flex gap-3 justify-end">
    <div class="order-1 max-w-[85%] ...">
      <div class="rounded-lg p-2.5 ... bg-primary text-primary-foreground shadow-sm"> ... </div> {/* UPDATED: shadow-sm */}
    </div>
  </div>

  {/* AI/Other Message (Left Aligned) */}
  <div class="flex gap-2.5 justify-start items-start">
    <Avatar size="sm" ... /> {/* size sm: h-6 w-6 */}
    <div class="max-w-[85%] ...">
      <div class="rounded-lg p-2.5 ... bg-secondary text-secondary-foreground shadow-sm"> {/* UPDATED: shadow-sm */}
        ...
        <div class="prose prose-sm mt-2 max-w-none"> {/* Add max-w-none to prose if needed */}
          <pre><code class="...">...</code></pre>
        </div>
      </div>
    </div>
  </div>
</div>

{/* Input Area */}
<div class="p-2 border-t border-border">
  <input type="text" class="w-full rounded-md ..." /> {/* UPDATED: rounded-md */}
</div>`;
    const messageBoxUsage = `// Use Flexbox for alignment.
// Use Avatar component (sm: h-6).
// Message bubbles: rounded-lg, padding, bg-primary/bg-secondary, shadow-sm.
// Use 'prose prose-sm max-w-none' for embedded formatted text/code.
// Outer container: overflow-y-auto, fixed height.

messages.map(msg => (
  <div key={msg.id} className={\`flex gap-3 \${msg.isUser ? 'justify-end' : 'justify-start items-start'}\`}>
    {!msg.isUser && <Avatar size="sm" />}
    <div className={\`max-w-[85%] \${msg.isUser ? 'order-1' : ''}\`}>
      <div className={\`rounded-lg p-2.5 text-sm shadow-sm ...\`}> ... </div>
    </div>
  </div>
))`;


    return (
        <main id="main-scroll-area" className="flex-1 overflow-y-auto p-6 lg:p-8 prose prose-slate max-w-none prose-headings:font-semibold prose-headings:text-foreground prose-a:text-primary hover:prose-a:text-primary/80 prose-code:before:content-none prose-code:after:content-none">
            <div className="max-w-5xl mx-auto space-y-16">

                {/* Overview Section */}
                <section id="overview">
                    <h2 className="flex items-center gap-2 not-prose text-2xl font-semibold border-b border-border pb-2 mb-6">
                         {/* Icon slightly larger */}
                        <Icon name="book-open" className="w-4 h-4 text-primary" /> Overview & Philosophy (v1.6)
                    </h2>
                    <p className="lead text-muted-foreground">React Design System v1.6. Refined minimalist aesthetic with a more monochromatic palette and smaller icons. Utility-first (Tailwind), inspired by Shadcn UI feel.</p>
                    <h3 className="text-xl font-semibold mt-6 mb-3">Core Principles</h3>
                     {/* Standard list style */}
                    <ul className="list-disc space-y-1 pl-5 text-muted-foreground text-sm">
                        <li>**Clarity:** Easy interpretation of UI elements.</li>
                        <li>**Consistency:** Predictable styling and interaction.</li>
                        <li>**Utility-First:** Tailwind CSS for styling.</li>
                        <li>**Minimalism:** Focus on function over decoration.</li>
                        <li>**Theming:** CSS variables for customization (more monochromatic).</li>
                    </ul>
                     <h3 className="text-xl font-semibold mt-6 mb-3">Technology Stack</h3>
                    <ul className="list-disc space-y-1 pl-5 text-muted-foreground text-sm">
                        <li>React (v18.x CDN)</li>
                        <li>Tailwind CSS (v3.x CDN + Typography)</li>
                        <li>Lucid Icons (CDN)</li>
                        <li>Monaco Editor (CDN)</li>
                        <li>Inter Font</li>
                    </ul>
                </section>

                {/* Foundations Section */}
                 <section id="foundations">
                     <h2 className="flex items-center gap-2 not-prose text-2xl font-semibold border-b border-border pb-2 mb-6">
                         {/* Icon slightly larger */}
                        <Icon name="layers" className="w-4 h-4 text-primary" />Foundations
                    </h2>
                     <p>Built upon CSS variables (see `:root` in HTML) mapped to a muted, monochromatic palette. Components leverage these variables and Tailwind utilities.</p>
                      <h3 className="text-xl font-semibold mt-6 mb-3">Typography & Spacing</h3>
                      <p>Uses Inter font. Base text size `text-sm` (14px). Spacing follows Tailwind's scale (`p-4`, `space-y-2`, etc.).</p>
                      <h3 className="text-xl font-semibold mt-6 mb-3">Iconography</h3>
                      <p>Uses Lucid Icons via the `<Icon/>` component. Default size is now `w-3.5 h-3.5`. Specific components or buttons might use slightly different sizes (e.g., `w-3 h-3` or `w-4 h-4`).</p>
                       <h3 className="text-xl font-semibold mt-6 mb-3">Radius & Shadow</h3>
                       <p>Standard border radius is `rounded-md` (6px, controlled by `--radius`). Cards use `rounded-lg`. Common shadow is `shadow-sm`.</p>
                 </section>

                {/* Layout Section */}
                <section id="layout">
                     <h2 className="flex items-center gap-2 not-prose text-2xl font-semibold border-b border-border pb-2 mb-6">
                         {/* Icon slightly larger */}
                        <Icon name="layout-template" className="w-4 h-4 text-primary" /> Layout
                    </h2>
                     <p>Flexbox layout: optional fixed sidebar (desktop), sticky header, scrollable main content, fixed footer. `MainContent` uses `prose` for docs, component previews use `not-prose`.</p>
                </section>

                 {/* Components Section */}
                <section id="components">
                    <h2 className="flex items-center gap-2 not-prose text-2xl font-semibold border-b border-border pb-2 mb-6">
                         {/* Icon slightly larger */}
                         <Icon name="puzzle" className="w-4 h-4 text-primary" /> Components
                    </h2>
                    <p className="text-muted-foreground mb-8">Core UI elements. Previews show appearance, Code/Usage tabs show implementation.</p>

                    {/* Render component previews using updated data */}
                     <ComponentPreview componentId="buttons" title="Buttons" description="Actions elements. Base '.button-60', variants (-primary, etc.), sizes (-sm, -xs)." previewContent={buttonPreview} codeContent={buttonCode} usageContent={buttonUsage} codeLanguage="html" usageLanguage="javascript" minHeight="350px"/>
                     <ComponentPreview componentId="cards" title="Cards" description="Content containers. Base '.card', padding utilities." previewContent={cardPreview} codeContent={cardCode} usageContent={cardUsage} codeLanguage="html" usageLanguage="html" minHeight="250px"/>
                     <ComponentPreview componentId="tags" title="Tags / Badges" description="Inline status/category indicators. Helper classes (.tag, .tag-*) or variable classes (.tag-primary, etc.)." previewContent={tagPreview} codeContent={tagCode} usageContent={tagUsage} codeLanguage="html" usageLanguage="javascript" minHeight="300px"/>
                     <ComponentPreview componentId="avatar" title="Avatar" description="User images/placeholders. Sizes: sm(h-6), md(h-7), lg(h-9)." previewContent={avatarPreview} codeContent={avatarCode} usageContent={avatarUsage} codeLanguage="javascript" usageLanguage="javascript" minHeight="280px"/>
                     <ComponentPreview componentId="userinfo" title="User Info Block" description="Combines Avatar (md: h-7), name/handle, optional actions (xs button)." previewContent={userInfoPreview} codeContent={userInfoCode} usageContent={userInfoUsage} codeLanguage="html" usageLanguage="javascript" minHeight="220px"/>
                     <ComponentPreview componentId="blockquote" title="Blockquote" description="Quoted text. Uses updated prose styles or utilities." previewContent={blockquotePreview} codeContent={blockquoteCode} usageContent={blockquoteUsage} codeLanguage="html" usageLanguage="html" minHeight="200px"/>
                     <ComponentPreview componentId="checkbox" title="Checkbox Switch" description="CSS-styled toggle switch. Uses updated styles." previewContent={checkboxPreview} codeContent={checkboxCode} usageContent={checkboxUsage} codeLanguage="html" usageLanguage="javascript" minHeight="300px"/>
                     <ComponentPreview componentId="messagebox" title="Message Box / Chat" description="Conversation layout. Uses Avatar (sm: h-6), styled bubbles (shadow-sm)." previewContent={messageBoxPreview} codeContent={messageBoxCode} usageContent={messageBoxUsage} codeLanguage="html" usageLanguage="javascript" minHeight="450px"/>
                     <ComponentPreview componentId="metadata" title="Metadata Display" description="Key-value list format. Uses smaller icons, muted tags." previewContent={metadataPreview} codeContent={metadataCode} usageContent={metadataUsage} codeLanguage="html" usageLanguage="html" minHeight="300px"/>
                     <ComponentPreview componentId="tables" title="Tables" description="Standard HTML tables styled with utilities. Uses updated buttons/tags." previewContent={tablePreview} codeContent={tableCode} usageContent={tableUsage} codeLanguage="html" usageLanguage="html" minHeight="350px"/>
                     <ComponentPreview componentId="collapse" title="Collapse Card (AI Steps)" description="Interactive sequence card. Uses updated status colors, icons, buttons." previewContent={collapsePreview} codeContent={collapseCode} usageContent={collapseUsage} codeLanguage="javascript" usageLanguage="javascript" minHeight="400px"/>
                     <ComponentPreview componentId="modal" title="Modal (Popup)" description="Overlay for tasks/details. Uses updated styles." previewContent={modalPreview} codeContent={modalCode} usageContent={modalUsage} codeLanguage="javascript" usageLanguage="javascript" minHeight="450px"/>
                     <ComponentPreview componentId="response" title="Response Panel" description="Final result display. Uses updated status colors/icons, buttons." previewContent={tweetPreview} codeContent={tweetCode} usageContent={tweetUsage} codeLanguage="html" usageLanguage="javascript" minHeight="450px"/>

                </section>

            </div> {/* End Content Wrapper */}
        </main>
    );
}


// --- Main App Component (Unchanged Logic) ---
function App() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalType, setModalType] = useState('example');
    const [modalData, setModalData] = useState(null);

    const handleOpenModal = (type = 'example', data = null) => {
        setModalType(type);
        setModalData(data);
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    // Initialize smooth scroll & initial static icons
    useEffect(() => {
        console.log("React App Initializing v1.6..."); // Version Bump Log

        const mainScrollArea = document.getElementById('main-scroll-area');
        const headerElement = document.querySelector('header');
        let headerHeight = headerElement ? headerElement.offsetHeight : 56;

        const resizeObserver = new ResizeObserver(entries => {
            for (let entry of entries) { headerHeight = entry.target.offsetHeight; }
        });
        if (headerElement) resizeObserver.observe(headerElement);

        const sidebarNav = document.querySelector('aside nav');
        const clickHandler = (e) => {
            const anchor = e.target.closest('a.nav-link');
            if (!anchor) return;
            const targetId = anchor.getAttribute('href');
            if (targetId && targetId.startsWith('#') && mainScrollArea) {
                e.preventDefault();
                const targetElement = document.getElementById(targetId.substring(1));
                if (targetElement) {
                    const elementTopInContainer = targetElement.offsetTop;
                    const scrollToPosition = elementTopInContainer - headerHeight - 24;
                    mainScrollArea.scrollTo({ top: Math.max(0, scrollToPosition), behavior: 'smooth' });
                }
            }
        };
        if (sidebarNav) sidebarNav.addEventListener('click', clickHandler);

        // Initial icon rendering delay
        const initialIconTimer = setTimeout(() => {
            try {
                 const staticIconNodes = document.querySelectorAll('aside [data-lucide]:not([data-rendered-by-react]), header [data-lucide]:not([data-rendered-by-react]), footer [data-lucide]:not([data-rendered-by-react]), section > h2 [data-lucide]:not([data-rendered-by-react])');
                 if (staticIconNodes.length > 0) {
                     lucide.createIcons({ nodes: Array.from(staticIconNodes) });
                     // console.log(`Rendered ${staticIconNodes.length} initial static icons.`);
                 }
            } catch (e) { console.error("Error rendering initial icons:", e); }
        }, 250);

        return () => {
            clearTimeout(initialIconTimer);
            if (sidebarNav) sidebarNav.removeEventListener('click', clickHandler);
            if (headerElement) resizeObserver.disconnect();
        };
    }, []);


    return (
        <div className="flex h-screen overflow-hidden bg-muted">
            <Sidebar />
            <div className="flex flex-1 flex-col overflow-hidden">
                <Header />
                <MainContent onOpenModal={handleOpenModal} />
                <Footer />
             </div>
            <Modal
                isOpen={isModalOpen}
                onClose={handleCloseModal}
                modalType={modalType}
                modalData={modalData}
             />
        </div>
    );
}


// --- Render the App AFTER Monaco is Ready (Unchanged Logic) ---
const rootElement = document.getElementById('root');
if (rootElement) {
    if (typeof require === 'function') {
        // console.log("Monaco loader 'require' found. Waiting for editor core...");
        require(['vs/editor/editor.main'], function() {
            // console.log("Monaco editor core loaded. Rendering React App...");
            try {
                const root = ReactDOM.createRoot(rootElement);
                root.render(<App />);
                console.log("React App v1.6 render initiated."); // Version Bump Log
            } catch (reactError) {
                 console.error("Error rendering React app:", reactError);
                 rootElement.innerHTML = '<p style="color: red; padding: 20px;">Error: Failed to render the React application.</p>';
            }
        }, function(error) {
            console.error("Failed to load Monaco editor core:", error);
            rootElement.innerHTML = '<p style="color: red; padding: 20px;">Error: Failed to load code editor component.</p>';
        });
    } else {
        console.error("Monaco loader 'require' is not defined. Cannot load editor or render app.");
         rootElement.innerHTML = '<p style="color: red; padding: 20px;">Critical Error: Code editor infrastructure failed to load.</p>';
    }
} else {
    console.error("Root element '#root' not found in the DOM.");
}