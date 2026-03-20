function disableContentCopy(e) {
	if (e && e.target && e.target.tagName ) {
		var tgName = e.target.tagName.toLowerCase();
		if (
			tgName === 'textarea'
			|| tgName === 'input'
			|| tgName === 'select'
			|| (
				e.target.classList
				&& e.target.classList.contains('emoji-wysiwyg-editor')
			)
			|| (
				e.target.hasAttribute('contenteditable')
				&& e.target.getAttribute('contenteditable')
			)
			|| e.target.classList.contains('gap-word')
		) {
			return true;
		}
	}
	return false;
}
document.ondragstart = disableContentCopy;
document.onselectstart = disableContentCopy;
document.oncontextmenu = disableContentCopy;
