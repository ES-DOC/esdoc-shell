#!/bin/bash
# ---------------------------------------------------------
# Minifies and merges all esdoc-js-client assets.
# ---------------------------------------------------------

# Display notice.
printf "*************************************\n"
printf "esdoc-js-client build :: STARTS\n"
printf "*************************************\n"

# ---------------------------------------------------------
# STEP 0 : Initialize.
# ---------------------------------------------------------

# Set version.
declare VERSION=$1
if [ ! "$VERSION" ]; then
    printf "!!! ERROR --> Build VERSION is required\n"
    exit -1
fi

# Set paths.
declare YUICOMPRESSOR=$DIR_BASH"/yuicompressor-2.4.7.jar"
declare SRC=$DIR_WEB_PLUGIN/src
declare BIN=$DIR_WEB_PLUGIN/bin

# Reset output folders.
rm -rf $BIN/latest
rm -rf $BIN/$VERSION
rm -rf $DIR_WEB_COMPARATOR'/src/media'
mkdir -p $BIN/latest/images
mkdir -p $BIN/$VERSION/images
mkdir -p $DIR_WEB_COMPARATOR'/src/media/images'

# Make tmp folders.
mkdir -p $DIR_TMP
mkdir -p $DIR_TMP/api
mkdir -p $DIR_TMP/core
mkdir -p $DIR_TMP/ext
mkdir -p $DIR_TMP/media/images
mkdir -p $DIR_TMP/tools
mkdir -p $DIR_TMP/tools/comparator/c1
mkdir -p $DIR_TMP/tools/comparator/views
mkdir -p $DIR_TMP/tools/search
mkdir -p $DIR_TMP/tools/viewer
mkdir -p $DIR_TMP/utils


# Set javascript fileset (N.B. order is important).
declare -a JS=(
    'ext/jquery.js'
    'ext/jquery.ui.js'
    'ext/underscore.js'
    'ext/backbone.js'
    'ext/jsExtensions.js'
    'ext/jquery.jsonp.js'
    'ext/numeral.js'
    'core/interface.js'
    'core/events.js'
    'core/options.js'
    'core/constants.js'
    'core/utils.js'
    'core/defaults.js'
    'utils/ontologies.js'
    'utils/ontologies.cim.v1.js'
    'utils/validation.js'
    'utils/view.button.js'
    'utils/view.buttonGroup.js'
    'utils/view.dialog.js'
    'utils/view.feedback.js'
    'utils/view.field.js'
    'utils/view.group.js'
    'utils/view.list.js'
    'utils/view.namedValue.js'
    'utils/view.separator.js'
    'api/main.js'
    'api/interface.js'
    'api/constants.js'
    'api/events.js'
    'api/utils.js'
    'api/parsers.js'
    'tools/viewer/main.js'
    'tools/viewer/interface.js'
    'tools/viewer/options.js'
    'tools/comparator/main.js'
    'tools/comparator/interface.js'
    'tools/comparator/events.js'
    'tools/comparator/views/componentTreeNode.js'
    'tools/comparator/views/componentTree.js'
    'tools/comparator/views/modelListItem.js'
    'tools/comparator/views/modelList.js'
    'tools/comparator/views/propertyTreeNode.js'
    'tools/comparator/views/propertyTree.js'
    'tools/comparator/c1/constants.js'
    'tools/comparator/c1/parser.js'
    'tools/comparator/c1/view.tab1ComponentTreeContent.js'
    'tools/comparator/c1/view.tab1ComponentTreeHeader.js'
    'tools/comparator/c1/view.tab1ModelListContent.js'
    'tools/comparator/c1/view.tab1ModelListHeader.js'
    'tools/comparator/c1/view.tab1PropertyTreeContent.js'
    'tools/comparator/c1/view.tab1PropertyTreeHeader.js'
    'tools/comparator/c1/view.tab1Toolbar.js'
    'tools/comparator/c1/view.tab1.js'
    'tools/comparator/c1/view.tab2Report.js'
    'tools/comparator/c1/view.tab2Summary.js'
    'tools/comparator/c1/view.tab2Toolbar.js'
    'tools/comparator/c1/view.tab2.js'
    'tools/comparator/c1/view.js'
    'tools/search/interface.js'
    'tools/search/constants.js'
    'tools/search/events.js'
    'utils/noConflict.js'
)

# Set CSS fileset.
declare -a CSS=('media/esdoc.css')

# Set Image filesets.
declare -a IMAGES=(
    'media/images/favicon.ico'
    'media/images/logo.png'
    'media/images/message.confirmation.png'
    'media/images/message.error.png'
    'media/images/message.help.png'
    'media/images/message.information.png'
    'media/images/message.warning.png'
)

# Set Legal notice.
declare DISCLAIMER="/*!
 * esdoc-js-client - javascript Library vVERSION
 * https://github.com/ES-DOC/esdoc-js-client
 *
 * Copyright YEAR, ES-DOC (http://es-doc.org)
 *
 * Licensed under the following licenses:.
 *     CeCILL       http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
 *     GPL v3       http://www.gnu.org/licenses/gpl.html
 *
 * Date: DATE
 */
"
declare DISCLAIMER=${DISCLAIMER/VERSION/$VERSION}
declare DISCLAIMER=${DISCLAIMER/YEAR/$(date +%Y)}
declare DISCLAIMER=${DISCLAIMER/DATE/$(date -u)}

# Set output targets.
declare -a jstargets=(
    $BIN'/latest/esdoc.js'
    $BIN'/'$VERSION'/esdoc.js'
    $DIR_WEB_COMPARATOR'/src/media/esdoc.js'
)
declare -a jstargets_min=(
    $BIN'/latest/esdoc-min.js'
    $BIN'/'$VERSION'/esdoc-min.js'
    $DIR_WEB_COMPARATOR'/src/media/esdoc-min.js'
)
declare -a csstargets=(
    $BIN'/latest/esdoc.css'
    $BIN'/'$VERSION'/esdoc.css'
    $DIR_WEB_COMPARATOR'/src/media/esdoc.css'
)
declare -a csstargets_min=(
    $BIN'/latest/esdoc-min.css'
    $BIN'/'$VERSION'/esdoc-min.css'
    $DIR_WEB_COMPARATOR'/src/media/esdoc-min.css'
)
declare -a imagetargets=(
    $BIN'/latest'
    $BIN'/'$VERSION
    $DIR_WEB_COMPARATOR'/src/media'
)

# ---------------------------------------------------------
# STEP 1 : Minimize.
# ---------------------------------------------------------
printf "Minifying ...\n"

# Minify js files.
printf "\tJS ...\n"
for f in "${JS[@]}"
do
	declare source="$SRC/$f"
	printf "\t\t%s\n" "$source"
	declare dest="$DIR_TMP/$f"
	java -jar $YUICOMPRESSOR $source -o $dest --nomunge
done

# Minify css files.
printf "\tCSS ...\n"
for f in "${CSS[@]}"
do
	declare source="$SRC/$f"
	declare dest="$DIR_TMP/$f"
	java -jar $YUICOMPRESSOR $source -o $dest --nomunge
	printf "\t\t%s\n" "$source"
done

# ---------------------------------------------------------
# STEP 2 : Transfer.
# ---------------------------------------------------------
printf "Transfering ...\n"

printf "\tJS ...\n"
for t in "${jstargets[@]}"
do
        echo -e "$DISCLAIMER" >> $t
        for f in "${JS[@]}"
        do
                file="$SRC/$f"
                cat $file >> $t
                echo -e "\n" >> $t
        done
	printf "\t\t%s\n" "$t"
done

printf "\tJS MINIFIED ...\n"
for t in "${jstargets_min[@]}"
do
        echo -e "$DISCLAIMER" >> $t
        for f in "${JS[@]}"
        do
                file="$DIR_TMP/$f"
                cat $file >> $t
        done
	printf "\t\t%s\n" "$t"
done

printf "\tCSS ...\n"
for t in "${csstargets[@]}"
do
        echo -e "$DISCLAIMER" >> $t
        for f in "${CSS[@]}"
        do
                file="$SRC/$f"
                cat $file >> $t
                echo -e "\n" >> $t
        done
	printf "\t\t%s\n" "$t"
done

printf "\tCSS MINIFIED ...\n"
for t in "${csstargets_min[@]}"
do
        echo -e "$DISCLAIMER" >> $t
        for f in "${CSS[@]}"
        do
                file="$DIR_TMP/$f"
                cat $file >> $t
        done
	printf "\t\t%s\n" "$t"
done

printf "\tIMAGES ...\n"
for t in "${imagetargets[@]}"
do
        for f in "${IMAGES[@]}"
        do
                file="$SRC/$f"
                dest=$t${f/media/}
                cp $file $dest
                printf "\t\t%s\n" "$dest"
        done
done

# Display notice.
printf "*************************************\n"
printf "esdoc-js-client build :: COMPLETE\n"
printf "*************************************\n"

exit 0
